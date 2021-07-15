import uuid

from .global_namespaces import namespaces

MAX_MESSAGE_LEN = 99


class _TestInfo:
    def __init__(self, report_data):
        self.report_data = report_data
        self.oval_definitions = self._get_oval_definitions()
        self.tests = self._get_tests()
        self.objects = self._get_objects_by_id()
        self.oval_system_characteristics = self._get_oval_system_characteristics()
        self.collected_objects = self._get_collected_objects_by_id()
        self.system_data = self._get_system_data_by_id()
        self.tests_info = self._get_tests_info()

    def _get_oval_system_characteristics(self):
        return self.report_data.find(
            ('.//XMLSchema:oval_results/XMLSchema:results/XMLSchema:system'
             '/oval-characteristics:oval_system_characteristics'), namespaces)

    @staticmethod
    def _get_data_by_id(data):
        return {item.attrib.get('id'): item for item in data}

    def _get_collected_objects_by_id(self):
        data = self.oval_system_characteristics.find(
            './/oval-characteristics:collected_objects', namespaces)
        return self._get_data_by_id(data)

    def _get_system_data_by_id(self):
        data = self.oval_system_characteristics.find(
            './/oval-characteristics:system_data', namespaces)
        return self._get_data_by_id(data)

    def _get_oval_definitions(self):
        return self.report_data.find(
            ('.//XMLSchema:oval_results/oval-definitions:oval_definitions'), namespaces)

    def _get_tests(self):
        return self.oval_definitions.find('.//oval-definitions:tests', namespaces)

    def _get_objects_by_id(self):
        data = self.oval_definitions.find(
            ('.//oval-definitions:objects'), namespaces)
        return self._get_data_by_id(data)

    @staticmethod
    def _get_key_of_xml_element(element):
        return element.tag.split('}')[1] if '}' in element.tag else element.tag

    @staticmethod
    def _find_item_ref(object_):
        list_of_item_ref = [item.get('item_ref') for item in object_]
        return list(filter(None, list_of_item_ref))

    @staticmethod
    def _get_unique_key(key):
        return key + '@' + str(uuid.uuid4())

    def _get_unique_id_in_dict(self, object_, dict_):
        if self._get_key_of_xml_element(object_) in dict_:
            return self._get_unique_key(self._get_key_of_xml_element(object_))
        return self._get_key_of_xml_element(object_)

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

    def _get_object_info(self, id_object):
        object_ = self.objects.get(id_object)
        collected_object = self.collected_objects.get(id_object)
        result = {}
        if collected_object is not None:
            result[
                collected_object.attrib.get('id')
            ] = collected_object.attrib.get('flag')
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
                elif self._get_key_of_xml_element(item) == 'message':
                    variable_value += self._complete_message(item, var_id) + '<br>'
        else:
            variable_value = 'no value'
        return variable_value

    @staticmethod
    def _complete_message(item, var_id):
        if len(item.text) == MAX_MESSAGE_LEN and var_id[:item.text.find('(')] in var_id:
            return "{}{})".format(item.text[:item.text.find('(') + 1], var_id)
        return item.text

    @staticmethod
    def _collected_object_is_not_none_and_contain_var_ref(element, collected_object):
        return collected_object is not None and 'var_ref' in element.attrib

    def _get_item(self, item_ref):
        item = self.system_data.get(item_ref)
        out = {}
        for element in item.iterchildren():
            if element.text and element.text.strip():
                out[self._get_unique_id_in_dict(element, out)] = element.text
        return out

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

    def get_info_about_test(self, id_of_test):
        for test in self.tests_info:
            if test['id'] == id_of_test:
                return test
        return None
