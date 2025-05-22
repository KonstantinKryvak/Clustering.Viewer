

import math,                       \
       numpy,                      \
       inspect,                    \
       dearpygui.dearpygui as dpg


g_ConcentrationObjects = []
g_InformationObjects   = []

g_Algorithms      = dict()
g_DistanceMetrics = dict()

def DefaultAlg():
    pass

def AddConcentrationPoint(sender, appdata, data):
    global g_ConcentrationObjects

    xpos = dpg.get_value('popup_x')
    ypos = dpg.get_value('popup_y')

    g_ConcentrationObjects.append([xpos, ypos])
    
    items = [f"({cx:.2f}, {cy:.2f})" for cx, cy in g_ConcentrationObjects]
    dpg.configure_item('listbox', items=items)

    for item in dpg.get_item_children('y_axis')[1]:
        dpg.delete_item(item)
    dpg.add_scatter_series(parent='y_axis', x=[x for x, _ in g_ConcentrationObjects], y=[y for _, y in g_ConcentrationObjects], label='Точки концентрації', tag='centers')

    dpg.hide_item('popup')


def GenConcentrationPoints(sender, appdata, data):
    global g_ConcentrationObjects

    amount = dpg.get_value('popup2_amount')

    x = numpy.random.rand(amount)
    y = numpy.random.rand(amount)

    g_ConcentrationObjects = list(zip(x, y))

    items = [f"({cx:.2f}, {cy:.2f})" for cx, cy in g_ConcentrationObjects]
    dpg.configure_item('listbox', items=items)

    for item in dpg.get_item_children('y_axis')[1]:
        dpg.delete_item(item)
    
    dpg.add_scatter_series(parent='y_axis', x=[cx for cx in x.tolist()], y=[cy for cy in y.tolist()], label='Точки концентрації', tag='centers')

    dpg.hide_item('popup2')


def RemoveConcentrationPoint(sender, appdata, data):
    global g_ConcentrationObjects

    selected = dpg.get_value('listbox')
    if not selected:
        return
    
    items = dpg.get_item_configuration('listbox')['items']
    idx = items.index(selected)
    g_ConcentrationObjects.pop(idx)
    items.pop(idx)
    
    dpg.configure_item('listbox', items=items)
    dpg.set_value('listbox', '')
    
    for item in dpg.get_item_children('y_axis')[1]:
        dpg.delete_item(item)

    dpg.add_scatter_series(parent='y_axis', x=[cx for cx, _ in g_ConcentrationObjects], y=[cy for _, cy in g_ConcentrationObjects], label='Початковий набір', tag='initial')


def GeneratePointSet(sender, app_data, user_data):
    global g_Algorithms, g_DistanceMetrics, g_InformationObjects, g_ConcentrationObjects

    amount = dpg.get_value('amount')
    scale = dpg.get_value('scale')

    if g_ConcentrationObjects:
        centers = numpy.array(g_ConcentrationObjects)

        idx = numpy.random.randint(0, len(centers),    size=amount)
        x   = numpy.random.normal(loc=centers[idx, 0], scale=scale)
        y   = numpy.random.normal(loc=centers[idx, 1], scale=scale)
    else:
        x = numpy.random.rand(amount)
        y = numpy.random.rand(amount)

    g_InformationObjects = list(zip(x, y))

    for item in dpg.get_item_children('y_axis')[1]:
        dpg.delete_item(item)
    dpg.add_scatter_series(parent='y_axis', x=[cx for cx in x.tolist()], y=[cy for cy in y.tolist()], label='Початковий набір', tag='initial')

    g_Algorithms, g_DistanceMetrics = user_data

    names = [key for key in g_Algorithms.keys()]
    dpg.configure_item('cls_alg', items=names, default_value=names[0])
    AlgorithmSelectionCallback(None, None, None)

    names = [key for key in g_DistanceMetrics.keys()]
    if names:
        dpg.configure_item('cls_dist', items=names, default_value=names[0], enabled=(len(names) > 1))
    else:
        dpg.configure_item('cls_dist', items=['default'], default_value='default', enabled=False)
    DistanceSelectionCallback(None, None, None)

    dpg.show_item('cls_group')


def AlgorithmSelectionCallback(sender, app_data, user_data):
    global g_Algorithms

    for tag in dpg.get_item_children('cls_alg_opts', slot=1):
        dpg.delete_item(tag)

    funcname = dpg.get_value('cls_alg')
    if not funcname or funcname == 'default':
        return

    sig = inspect.signature(g_Algorithms.get(funcname, DefaultAlg))

    for name, param in sig.parameters.items():
        if name not in ['points', 'dist_metric', 'distance', 'metric']:
            dpg.add_spacer(parent='cls_alg_opts')
            dpg.add_text(f'Параметр \"{name}\":', parent='cls_alg_opts')
            if param.annotation is int:
                dpg.add_input_int(default_value=param.default, parent='cls_alg_opts', tag=name, width=-1)
            elif param.annotation is float:
                dpg.add_input_float(default_value=param.default, parent='cls_alg_opts', tag=name, width=-1)

    dpg.show_item('cls_alg_opts')


def DistanceSelectionCallback(sender, app_data, user_data):
    global g_DistanceMetrics

    for tag in dpg.get_item_children('cls_dist_opts', slot=1):
        dpg.delete_item(tag)

    funcname = dpg.get_value('cls_dist')
    if (not funcname or (funcname == 'default')):
        return

    sig = inspect.signature(g_DistanceMetrics.get(funcname, DefaultAlg))

    for name, param in sig.parameters.items():
        if name not in ['first', 'second', 'point1', 'point2', 'p1', 'p2', 'src', 'dst']:
            dpg.add_spacer(parent='cls_dist_opts')
            dpg.add_text(f'Параметер {name}:', parent='cls_dist_opts')
            dpg.add_input_int(label=name, default_value=0, parent='cls_dist_opts', width=-1)

    dpg.show_item('cls_dist_opts')


def DoClusteringCallback(sender, app_data, user_data):
    global g_Algorithms, g_DistanceMetrics, g_InformationObjects

    algorithm = g_Algorithms.get(dpg.get_value('cls_alg'), None)
    if not algorithm:
        return
    
    metric = g_DistanceMetrics.get(dpg.get_value('cls_dist'), None)
    if not metric:
        metric = lambda p1, p2: numpy.sqrt(sum((x - y) ** 2 for x, y in zip(p1, p2)))

    dpg.configure_item('btn_gen', enabled=False)
    dpg.configure_item('do_cls',  enabled=False)

    args = []
    for tag in dpg.get_item_children('cls_alg_opts', slot=1):
        value = dpg.get_value(tag)
        if value and (not isinstance(value, str)):
            args.append(value)

    result = algorithm(g_InformationObjects, metric, *(arg for arg in args))

    clusters = dict()
    for index, object in enumerate(g_InformationObjects):
        clusters.setdefault(result[index], []).append(object)

    for item in dpg.get_item_children('y_axis')[1]:
        dpg.delete_item(item)

    for key, values in clusters.items():
        dpg.add_scatter_series(parent='y_axis', x=[x for x, _ in values], y=[y for _, y in values], label='Визначені як шум' if (key == -1) else f'Кластер No. {key + 1}')

    dpg.configure_item('btn_gen', enabled=True)
    dpg.configure_item('do_cls',  enabled=True)


