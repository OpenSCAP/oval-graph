import graph.oval_graph
import collections
import re
import uuid


class converter():
    def __init__(self, tree):
        self.VALUE_TO_BOOTSTRAP_COLOR = {
            "true": "text-success",
            "false": "text-danger",
            "error": "text-dark",
            "unknown": "text-dark",
            "noteval": "text-dark",
            "notappl": "text-dark"
        }

        self.VALUE_TO_ICON = {
            "true": "glyphicon glyphicon-ok",
            "false": "glyphicon glyphicon-remove",
            "error": "glyphicon glyphicon-question-sign",
            "unknown": "glyphicon glyphicon-question-sign",
            "noteval": "glyphicon glyphicon-question-sign",
            "notappl": "glyphicon glyphicon-question-sign"
        }

        self.VALUE_TO_HEX_COLOR = {
            "true": "#00ff00",
            "false": "#ff0000",
            "error": "#000000",
            "unknown": "#000000",
            "noteval": "#000000",
            "notappl": "#000000"
        }

        if isinstance(tree, graph.oval_graph.OvalNode):
            self.tree = tree
        else:
            raise ValueError('err - this is not tree created from OvalNodes')

    def _get_node_icon(self):
        values = self._get_node_style()
        return dict(
            color=self.VALUE_TO_BOOTSTRAP_COLOR[values['negation_color']],
            icon=self.VALUE_TO_ICON[values['out_color']],
        )

    def get_comment(self):
        if self.tree.comment is not None:
            return str(self.tree.comment)
        return ""

    def to_JsTree_dict(self):
        icons = self._get_node_icon()
        out = {
            'text': '<strong><span class="' + icons['color'] + '">' +
                    self._get_label() + '</span></strong>' +
                    ' <i>' + self.get_comment() + '</i>',
            "icon": icons['icon'] + ' ' + icons['color'],
            "state": {
                    "opened": True}}
        if self.tree.children:
            out['children'] = [converter(child).to_JsTree_dict()
                               for child in self.tree.children]
        return out

    def _get_node_style(self):
        value = self.tree.evaluate_tree()
        out_color = None
        if value is None:
            if self._is_negated_boolean('true', self.tree.value):
                out_color = 'false'
            elif self._is_negated_boolean('false', self.tree.value):
                out_color = 'true'
            else:
                out_color = self.tree.value
            out_color, value = self.tree.value, out_color
        else:
            if self._is_negated_boolean('true', value):
                out_color = 'false'
            elif self._is_negated_boolean('false', value):
                out_color = 'true'
            else:
                out_color = value
        return dict(
            negation_color=value,
            out_color=out_color,
        )

# Methods for interpreting oval tree with SigmaJS

    def _get_label(self):
        if self.tree.node_type == 'value':
            return re.sub(
                '(oval:ssg-test_|oval:ssg-)|(:def:1|:tst:1)', '', str(self.tree.node_id))
        else:
            if str(self.tree.node_id).startswith('xccdf_org'):
                return re.sub(
                    '(xccdf_org.ssgproject.content_)', '', str(
                        self.tree.node_id))
            return self.tree.value

    def _is_negated_boolean(self, boolean, value):
        if value == boolean and self.tree.negation:
            return True
        return False

    def _get_node_colors(self):
        values = self._get_node_style()
        return dict(
            color=self.VALUE_TO_HEX_COLOR[values['negation_color']],
            borderColor=self.VALUE_TO_HEX_COLOR[values['out_color']],
        )

    def _get_node_title(self):
        value = self.tree.evaluate_tree()
        if value is None:
            value = self.tree.value
        if value == 'true' or value == 'false':
            return self.tree.node_id
        return str(self.tree.node_id) + ' ' + self.tree.value

    def _create_node(self, x, y):
        # print(self.evaluate_tree(),self.value)
        colors = self._get_node_colors()
        return {
            'id': self.tree.node_id,
            'label': self._get_label(),
            'url': 'null',
            'text': self.tree.comment,
            'title': self._get_node_title(),
            "x": x,
            "y": y,
            "size": 3,
            "color": colors['color'],
            "type": "circle",
            "borderColor": colors['borderColor']}

    def _create_edge(self, id_source, id_target, target_node):
        return {
            "id": str(uuid.uuid4()),
            "source": id_source,
            "target": id_target,
            "color": self._get_color_edge(target_node)
        }

    def _get_color_edge(self, target_node):
        return target_node['color']

    def create_list_of_id(self, array_of_ids=None):
        if array_of_ids is None:
            array_of_ids = []
            array_of_ids.append(self.tree.node_id)
        for child in self.tree.children:
            if child.node_type != "operator":
                array_of_ids.append(child.node_id)
            else:
                array_of_ids.append(child.node_id)
                converter(child).create_list_of_id(array_of_ids)
        return array_of_ids

    def _remove_Duplication(self, graph_data):
        array_of_ids = self.create_list_of_id()
        out = dict(nodes=[], edges=graph_data['edges'])
        duplicate_ids = [item for item, count in collections.Counter(
            array_of_ids).items() if count > 1]

        for node in graph_data['nodes']:
            if node['id'] not in duplicate_ids:
                out['nodes'].append(node)

        for id in duplicate_ids:
            for node in graph_data['nodes']:
                if node['id'] == id:
                    out['nodes'].append(node)
                    break
        return out

    def _fix_graph(self, preprocessed_graph_data):
        for node in preprocessed_graph_data['nodes']:
            for node1 in preprocessed_graph_data['nodes']:
                if node['x'] == node1['x'] and node['y'] == node1['y']:
                    node['x'] = node['x'] - 1
        return preprocessed_graph_data

    def _help_to_sigma_dict(self, x, y, preprocessed_graph_data=None):
        if preprocessed_graph_data is None:
            preprocessed_graph_data = dict(nodes=[], edges=[])
            preprocessed_graph_data['nodes'].append(self._create_node(x, y))
        y_row = y + 1
        x_row = x
        for node in self.tree.children:
            preprocessed_graph_data['nodes'].append(
                converter(node)._create_node(x_row, y_row))
            preprocessed_graph_data['edges'].append(converter(node)._create_edge(
                self.tree.node_id, node.node_id, preprocessed_graph_data['nodes'][-1]))
            x_row = x_row + 1
            if node.children is not None:
                preprocessed_graph_data = converter(node)._help_to_sigma_dict(
                    x_row + 1, y_row + 1, preprocessed_graph_data)
        return self._fix_graph(preprocessed_graph_data)

    def _count_max_y(self, out):
        max_y = 0

        for node in out['nodes']:
            if max_y < node['y']:
                max_y = node['y']
        return max_y

    def _create_nodes_in_rows(self, rows):
        nodes_in_rows = dict()

        for i in range(rows + 1):
            nodes_in_rows[i] = []
        return nodes_in_rows

    def _push_nodes_to_nodes_in_row(self, out, nodes_in_rows):
        for node in out['nodes']:
            nodes_in_rows[node['y']].append(node)

    def _remove_empty_rows(self, nodes_in_rows, max_y):
        for row in range(max_y + 1):
            if not nodes_in_rows[row]:
                del nodes_in_rows[row]

    def _move_rows(self, nodes_in_rows):
        count = 0
        nodes_in_rows1 = dict()

        for row in nodes_in_rows:
            nodes_in_rows1[count] = nodes_in_rows[row]
            for node in nodes_in_rows1[count]:
                node['y'] = count
            count += 1
        return nodes_in_rows1

    def _create_positions(self, nodes_in_rows):
        positions = []
        for row in nodes_in_rows:
            len_of_row = len(nodes_in_rows[row])
            if len_of_row > 1:
                if (len_of_row % 2) == 1:
                    len_of_row += 1

                for i in range((int(-(len_of_row / 2))) * 2,
                               (int(+(len_of_row / 2)) + 1) * 2, 2):
                    positions.append(i)

                if len_of_row == 2:
                    positions.remove(0)

                if len(nodes_in_rows[row]) < len(positions):
                    positions.pop()
                    if len(nodes_in_rows[row]) < len(positions):
                        positions.pop(0)

                count = 0

                for pos in positions:
                    nodes_in_rows[row][count]['x'] = pos
                    count += 1
                positions = []
            else:
                nodes_in_rows[row][0]['x'] = 0

        return positions

    def _convert_nodes_in_rows_to_nodes(self, nodes_in_rows):
        nodes = []
        for row in nodes_in_rows:
            for node in nodes_in_rows[row]:
                nodes.append(node)
        return nodes

    def _change_position(self, nodes_in_rows):
        x = 0.6
        up_and_down = True
        down = False
        down_row = False
        save_x = 0
        continue_move = False

        for row in nodes_in_rows:
            for node in nodes_in_rows[row]:
                if (len(node['label']) > 6
                        and len(node['label']) < 40
                        or continue_move):
                    if up_and_down:
                        node['y'] = node['y'] + (0.6 * x)
                        up_and_down = False
                    else:
                        up_and_down = True
                    continue_move = True
                elif len(node['label']) > 30:
                    node['y'] = node['y'] + (0.6 * x)
                    x += 0.6
                    save_x = x
                    down = True
                else:
                    if down:
                        node['y'] = node['y'] + (0.6 * save_x)

                    if down_row:
                        node['y'] = node['y'] + (0.6 * save_x) - 0.7
            if down:
                down = False
                down_row = True
            continue_move = False
            x = 0.6

    def _sort(self, array):
        less = []
        equal = []
        greater = []

        if len(array) > 1:
            pivot = array[0]['x']
            for node in array:
                if node['x'] < pivot:
                    less.append(node)
                if node['x'] == pivot:
                    equal.append(node)
                if node['x'] > pivot:
                    greater.append(node)
            return self._sort(less) + equal + self._sort(greater)
        else:
            return array

    def _sort_nodes(self, nodes_in_rows):
        for row in nodes_in_rows:
            nodes_in_rows[row] = self._sort(nodes_in_rows[row])

    def _center_graph(self, out):
        max_y = self._count_max_y(out)
        nodes_in_rows = self._create_nodes_in_rows(max_y)
        self._push_nodes_to_nodes_in_row(out, nodes_in_rows)
        self._remove_empty_rows(nodes_in_rows, max_y)
        nodes_in_rows = self._move_rows(nodes_in_rows)
        self._sort_nodes(nodes_in_rows)
        self._create_positions(nodes_in_rows)
        self._change_position(nodes_in_rows)
        out['nodes'] = self._convert_nodes_in_rows_to_nodes(nodes_in_rows)
        return out

    def to_sigma_dict(self, x, y):
        return self._center_graph(
            self._remove_Duplication(
                self._help_to_sigma_dict(
                    x, y)))
