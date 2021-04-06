import uuid

ns = {
    'XMLSchema': 'http://oval.mitre.org/XMLSchema/oval-results-5',
    'xccdf': 'http://checklists.nist.gov/xccdf/1.2',
    'arf': 'http://scap.nist.gov/schema/asset-reporting-format/1.1',
    'oval-definitions': 'http://oval.mitre.org/XMLSchema/oval-definitions-5',
    'scap': 'http://scap.nist.gov/schema/scap/source/1.2',
    'oval-characteristics': 'http://oval.mitre.org/XMLSchema/oval-system-characteristics-5',
}


class _XmlParserTestInfo:
    def __init__(self, report_data):
        self.report_data = report_data
        self.oval_definitions = self._get_oval_definitions()
        self.tests = self._get_tests()
        self.objects = self._get_objects()
        self.collected_objects = self._get_collected_objects()
        self.system_data = self._get_system_data()
        self.tests_info = self._get_tests_info()

    def _get_collected_objects(self):
        data = self.report_data.find(
            ('.//XMLSchema:oval_results/XMLSchema:results/'
             'XMLSchema:system/oval-characteristics:oval_system_characteristics'
             '/oval-characteristics:collected_objects'), ns)
        out = {}
        for item in data:
            out[item.attrib.get('id')] = item
        return out

    def _get_system_data(self):
        data = self.report_data.find(
            ('.//XMLSchema:oval_results/XMLSchema:results/'
             'XMLSchema:system/oval-characteristics:oval_system_characteristics'
             '/oval-characteristics:system_data'), ns)
        out = {}
        for item in data:
            out[item.attrib.get('id')] = item
        return out

    def _get_oval_definitions(self):
        data = self.report_data.find(
            ('.//XMLSchema:oval_results/oval-definitions:oval_definitions'), ns)
        return data

    def _get_tests(self):
        data = self.oval_definitions.find(
            ('.//oval-definitions:tests'), ns)
        return data

    def _get_objects(self):
        data = self.oval_definitions.find(
            ('.//oval-definitions:objects'), ns)
        out = {}
        for item in data:
            out[item.attrib.get('id')] = item
        return out

    def _get_key_for_element(self, element):
        return element.tag.split('}')[1] if '}' in element.tag else element.tag

    def _find_item_ref(self, object_):
        return list(
            filter(
                None, [
                    self._get_item_ref(item) for item in object_]))

    def _get_item_ref(self, item):
        return item.get('item_ref') if item.get('item_ref') else None

    def _get_unique_key(self, key):
        return key + '@' + str(uuid.uuid4())

    def _get_unique_id_in_dict(self, object_, dict_):
        if self._get_key_for_element(object_) in dict_:
            return self._get_unique_key(self._get_key_for_element(object_))
        else:
            return self._get_key_for_element(object_)

    def _get_collected_objects_info(self, collected_object, object_):
        out = {}
        if len(collected_object) == 0:
            out[self._get_unique_id_in_dict(object_, out)
                ] = self._get_object_items(object_, collected_object)
        else:
            item_refs = self._find_item_ref(collected_object)
            if item_refs:
                for item_id in item_refs:
                    out[self._get_unique_id_in_dict(
                        object_, out)] = self._get_item(item_id)
            else:
                out[self._get_unique_id_in_dict(
                    object_, out)] = self._get_object_items(object_, collected_object)
        return out

    def _xml_element_to_dict(self, object_, collected_object):
        result = {}
        if collected_object is not None:
            result[
                collected_object.attrib.get('id')
            ] = collected_object.attrib.get('flag')
            out = {}
            result.update(
                self._get_collected_objects_info(collected_object, object_))
        else:
            result[object_.attrib.get('id')] = "does not exist"
            result[self._get_unique_id_in_dict(
                object_, result)] = self._get_object_items(object_, collected_object)
        return result

    def _get_object_items(self, object_, collected_object):
        out = {}
        for element in object_.iterchildren():
            if element.text and element.text.strip():
                out[self._get_unique_id_in_dict(element, out)] = element.text
            else:
                out[self._get_unique_id_in_dict(element, out)] = self._get_ref_var(
                    element, collected_object)
        return out

    def _get_ref_var(self, element, collected_object):
        variable_value = ''
        if self._collected_object_is_not_none_and_contain_var_ref(
                element, collected_object):
            var_id = element.attrib.get('var_ref')
            for item in collected_object:
                if var_id == item.attrib.get('variable_id'):
                    variable_value += item.text
                elif self._get_key_for_element(item) == 'message':
                    variable_value += self._fix_message(item, var_id) + '<br>'
        else:
            variable_value = 'no value'
        return variable_value

    def _fix_message(self, item, var_id):
        if len(
                item.text) == 99 and var_id[:99 - item.text.find('(')] in var_id:
            return item.text[:item.text.find('(') + 1] + var_id + ')'
        return item.text

    def _collected_object_is_not_none_and_contain_var_ref(
            self, element, collected_object):
        if collected_object is not None and 'var_ref' in element.attrib:
            return len(collected_object)
        return False

    def _get_item(self, item_ref):
        item = self._find_item_by_id(self.system_data, item_ref)
        out = {}
        for element in item.iterchildren():
            if element.text and element.text.strip():
                out[self._get_unique_id_in_dict(element, out)] = element.text
        return out

    def _find_item_by_id(self, items, id):
        if id in items.keys():
            return items[id]
        return None

    def _get_object_info(self, id_object):
        object_ = self._find_item_by_id(self.objects, id_object)
        object_collected = self._find_item_by_id(
            self.collected_objects, id_object)
        return self._xml_element_to_dict(object_, object_collected)

    def _get_tests_info(self):
        out = []
        for test in self.tests:
            objects = []
            for item in test:
                object_id = item.attrib.get('object_ref')
                if object_id:
                    objects.append(self._get_object_info(object_id))
            out.append(
                dict(
                    id=test.attrib.get('id'),
                    comment=test.attrib.get('comment'),
                    objects=objects,
                ))
        return out

    def get_info_about_test(self, id):
        for test in self.tests_info:
            if test['id'] == id:
                return test
