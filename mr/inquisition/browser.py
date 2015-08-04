import re

from Products.Five import BrowserView
from Acquisition import aq_inner, aq_base, aq_chain


class Product(object):
    """Class to represent the products."""

    def __init__(self, product_id):
        self.id = product_id
        self.content_types = []
        self.installed = False

    def __cmp__(self, other):
        return cmp(self.id, other.id)


class ContentType(object):
    """Class to store the content types we find."""

    def __init__(self, portal_type, title, meta_type, product_id):
        self.portal_type = portal_type
        self.title = title
        self.meta_type = meta_type
        self.product_id = product_id
        self.number = 0

    def _cmp_type(self):
        type_str = ''
        if self.portal_type:
            type_str += self.portal_type
        type_str += self.meta_type
        return type_str

    def __cmp__(self, other):
        return cmp(self._cmp_type(), other._cmp_type())


class ContentObject(object):
    """Class to store the data about the objects we find."""

    def __init__(self, title, url='', size=0):
        self.title = title
        self.url = url
        self.size = size

    def __cmp__(self, other):
        return cmp(self.title, other.title)


class ContentMatrix(BrowserView):
    """This view will display a matrix with the content types as one
    axis and the folders where they are locate in on the other.
    """

    def title(self):
        return 'Content types vs. Folders Matrix'

    def raw(self):
        return 'raw' in self.request.form

    def thousands(self, x):
        """Add dots as thousands separator. Works only on ints.
        Taken from http://code.activestate.com/recipes/498181/
        """
        if self.raw():
            return x
        return re.sub(r'(\d{3})(?=\d)', r'\1.', str(x)[::-1])[::-1]

    def _find_objects_in_location(self, location, size=False):
        """Return a dict with the found meta types as keys and the
        number of objects as values.
        """
        found_objects = {}
        for id, obj in location.ZopeFind(location,
                                         search_sub=True):
            obj = aq_base(obj)
            try:
                meta_type = obj.meta_type
            except AttributeError:
                continue

            # Are we counting the number of items, or the size of the items?
            if not size:
                counter = 1
            else:
                try:
                    counter = obj.get_size()
                except AttributeError:
                    counter = 0

            if meta_type in found_objects:
                found_objects[meta_type] += counter
            else:
                found_objects[meta_type] = counter
        return found_objects

    def _object_types_per_folder(self, size=False):
        """Return all the objects for every folderish object in the current
        context.
        """
        context = aq_inner(self.context)
        found_objects = {}
        for item in context.objectValues():
            try:
                if item.isPrincipiaFolderish and item.meta_type:
                    found_objects[item.getId()] = \
                        self._find_objects_in_location(item, size)
            except AttributeError:
                # This item doesn't have a meta_type.
                pass
        return found_objects

    def _portal_types_types(self):
        """Return a list of content types as found in the portal types."""
        types = []
        context = aq_inner(self.context)
        types_tool = context.portal_types
        for ptype in types_tool.listContentTypes():
            info = types_tool.getTypeInfo(ptype)
            ct = ContentType(ptype,
                             info.title,
                             info.content_meta_type,
                             info.product)
            types.append(ct)
        return types

    def _known_content_types(self):
        """Return all content types: based on the portal types tool and
        the actual content.
        """
        # Get the content types from the portal types tool
        types = self._portal_types_types()

        # Complement the types from the types tool with the types found
        # by processing the site.
        found_objects = self._object_types_per_folder()
        all_types = set()
        for folder in found_objects:
            content_types = found_objects[folder].keys()
            all_types.update(set(content_types))
        # Remove the already known types.
        types_set = all_types.copy()
        for ct in types:
            if not ct.product_id:
                ct.product_id = 'Unknown'
            if ct.meta_type in types_set:
                types_set.remove(ct.meta_type)
        # Create new ContentType instances for the remaining types.
        for mtype in types_set:
            new_ct = ContentType(None, None, mtype, 'Unknown')
            types.append(new_ct)
        return types

    def _products(self):
        """Return a list of all products, based on the content."""
        types = self._known_content_types()
        products = {}
        for ct in types:
            if ct.product_id not in products:
                products[ct.product_id] = Product(ct.product_id)
            products[ct.product_id].content_types.append(ct)
        product_ids = products.keys()
        product_ids.sort()
        if 'Unknown' in product_ids:
            idx = product_ids.index('Unknown')
            product_ids = (product_ids[:idx] + product_ids[idx + 1:] +
                           [product_ids[idx]])
        result = []
        for product_id in product_ids:
            product = products[product_id]
            product.content_types.sort()
            result.append(product)
        return result

    def folders(self):
        """Return the list of folders."""
        folders = self._object_types_per_folder().keys()
        folders.sort()
        return folders

    def type_per_folder(self, size=False):
        """Return a complete row of portal type information."""
        folders = self.folders()
        types_per_folder = self._object_types_per_folder(size)
        products = self._products()
        grand_total = 0
        total_per_folder = {}
        for product in products:
            for contenttype in product.content_types:
                output = [product.id]
                if contenttype.portal_type:
                    output.append(contenttype.portal_type)
                else:
                    output.append(contenttype.meta_type + '&nbsp;[1]')
                total = 0
                meta_type = contenttype.meta_type
                for folder in folders:
                    if (meta_type not in types_per_folder[folder] or
                            types_per_folder[folder][meta_type] == 0):
                        output.append('&nbsp;')
                    else:
                        number = types_per_folder[folder][meta_type]
                        output.append(self.thousands(number))
                        if folder not in total_per_folder:
                            total_per_folder[folder] = 0
                        total_per_folder[folder] += number
                        total += number
                output[2:2] = [self.thousands(total)]
                grand_total += total
                yield output
        output = ['total', '&nbsp', self.thousands(grand_total)]
        for folder in folders:
            output.append(self.thousands(total_per_folder.get(folder, 0)))
        yield output


class ContentMatrixSize(ContentMatrix):
    """This view will display a matrix with the content types as one
    axis and the folders where they are locate in on the other.

    The number that is displayed is the size of the objects.
    """

    def title(self):
        return 'Content type sizes vs. Folders Matrix'

    def type_per_folder(self, size=True):
        return super(ContentMatrixSize, self).type_per_folder(size=True)


class CountTypes(ContentMatrix):
    """This view will list the portal types (grouped per product) and
    how many objects per type are found in the site.
    """

    def _object_types_in_site(self):
        """Return all the number of objects in the site, grouped by
        meta type.
        """
        portal = self.context.portal_url.getPortalObject()
        return self._find_objects_in_location(portal)

    def _products_dict(self):
        """Return a dict of products in the site.
        The product IDs are the keys, the constructed Products the values.
        """
        qi_tool = self.context.portal_quickinstaller
        products = {}
        control_panel_products = \
            self.context.Control_Panel.Products.objectIds()
        # Get all installable products
        for product_id in control_panel_products:
            if qi_tool.isProductInstallable(product_id):
                product = Product(product_id)
                product.installed = qi_tool.isProductInstalled(product_id)
                products[product_id] = product
        # Some products aren't installable as such, but *are* available.
        for product_id, product_obj in qi_tool.items():
            if product_id not in products:
                product = Product(product_id)
                product.installed = qi_tool.isProductInstalled(product_id)
                products[product_id] = product
        return products

    def summary(self):
        """Return a summary of the found products."""
        products = self.products()
        products_number = len(products)
        objects = 0
        for product in products:
            for content_type in product.content_types:
                objects += content_type.number
        return dict(products = products_number,
                    objects = objects)

    def products(self):
        """Return a list of products in the site."""
        types = self._portal_types_types()
        products = self._products_dict()
        objects = self._object_types_in_site()
        for pt_type in types:
            if pt_type.product_id in products:
                if pt_type.meta_type in objects:
                    pt_type.number = objects[pt_type.meta_type]
                products[pt_type.product_id].content_types.append(pt_type)
                products[pt_type.product_id].content_types.sort()
        products = products.values()
        products.sort()
        return products


class ListObjectSizes(ContentMatrix):
    """Create an enormous list of all objects and their size.
    For folderish types accumulate the children's sizes.
    """

    def list_objects(self):
        """Depth first search of the current context to calculate object sizes.
        Returns a sorted list of ContentObjects.
        """
        to_visit = [self.context]
        visited = {}

        while to_visit:
            context = to_visit.pop()
            children = context.getChildNodes()

            if children:
                to_visit.extend(children)

            try:
                current_size = context.get_size()
            except AttributeError:
                current_size = 0

            visited[context.absolute_url_path()] = ContentObject(
                title=context.absolute_url_path(),
                url=context.absolute_url(),
                size=current_size)

            for parent in aq_chain(context):
                try:
                    parent_path = parent.absolute_url_path()
                except AttributeError:
                    # Doesn't have a path -> no proper object we want to count.
                    # We assume it's this view and we don't need to traverse
                    # the aq_chain further up.
                    break
                if parent_path in visited and not parent == context:
                    visited[parent_path].size += current_size
        return sorted(visited.values())
