

from .         import ActionCallbacks as callbacks
from dearpygui import dearpygui       as dpg


def Init():
    dpg.create_context()

    LoadDefaultSystemFont()
    SetupStyleTheme()


def LoadDefaultSystemFont():
    with dpg.font_registry():
        with dpg.font('C:\\Windows\\Fonts\\segoeui.ttf', 18) as font:
            dpg.add_font_range_hint(dpg.mvFontRangeHint_Cyrillic)
            dpg.bind_font(font)


def SetupStyleTheme():
     with dpg.theme() as theme:
        with dpg.theme_component(dpg.mvAll):
            dpg.add_theme_style(dpg.mvStyleVar_WindowPadding, x=0, y=0)


def SetupInitialLayout(metrics, algorithms):
    with dpg.window(tag='main', width=-1, height=-1):
        with dpg.group(horizontal=True):
            
            with dpg.child_window(tag='ctrl_window', width=384, autosize_y=True, border=False):
                with dpg.group(tag='io_group', horizontal=False, show=True):
                    dpg.add_separator(label='Генерація Тестових Наборів')
                    
                    dpg.add_spacer()
                    dpg.add_text('Ліміт амплітуди генерації:')
                    
                    dpg.add_spacer()
                    with dpg.group(horizontal=True):
                        dpg.add_text('Для вісі OX:')
                        dpg.add_input_float(tag='ox_limit', default_value=20.0, min_value=1.0, max_value=1000.0, width=-1)
                    with dpg.group(horizontal=True):
                        dpg.add_text('Для вісі OY:')
                        dpg.add_input_float(tag='oy_limit', default_value=20.0, min_value=1.0, max_value=1000.0, width=-1)
                    
                    dpg.add_spacer()
                    dpg.add_text('Кількість об\'єктів (N):')
                    dpg.add_input_int(tag='amount', default_value=250, min_value=0, width=-1)
                    
                    dpg.add_spacer()
                    dpg.add_text('Зміщення генерації (scale/sigma):')
                    dpg.add_input_float(tag='scale', default_value=0.1, min_value=0, width=-1)
                    
                    dpg.add_text('Точки концентрації:')
                    dpg.add_listbox(items=[], tag='listbox', num_items=6)
                    dpg.add_button(label='Додати точку концентрації',      width=-1,    callback=lambda: dpg.show_item('popup'))
                    dpg.add_button(label='Згенерувати набір концентрації', width=-1,    callback=lambda: dpg.show_item('popup2'))
                    dpg.add_button(label='Прибрати точку концентрації',    width=-1,    callback=callbacks.RemoveConcentrationPoint)
                    
                    dpg.add_spacer(height=32)
                    
                    dpg.add_button(label='Утворити Тестовий Набір', tag='btn_gen', width=-1, callback=callbacks.GeneratePointSet, user_data=(algorithms, metrics))
                    dpg.add_spacer()

                with dpg.group(tag='cls_group', horizontal=False, show=False):  
                    dpg.add_separator(label='Кластеризація')

                    dpg.add_spacer()
                    dpg.add_text('Метрика відстані:')
                    dpg.add_combo(items=[], tag='cls_dist', callback=callbacks.DistanceSelectionCallback,  width=-1)
                    dpg.add_separator()
                    with dpg.group(tag='cls_dist_opts', show=False):
                        pass

                    dpg.add_spacer()
                    dpg.add_text('Алгоритм кластеризації:')
                    dpg.add_combo(items=[], tag='cls_alg',  callback=callbacks.AlgorithmSelectionCallback, width=-1)
                    dpg.add_separator()
                    with dpg.group(tag='cls_alg_opts', show=False):
                        pass

                    dpg.add_spacer(height=32)
                    dpg.add_button(label='Виконати кластеризацію', tag='do_cls', callback=callbacks.DoClusteringCallback, width=-1)
            
            with dpg.child_window(autosize_x=True, autosize_y=True, tracked=True):
                with dpg.plot(label='Результати', height=-1, width=-1):
                    dpg.add_plot_legend()
                    dpg.add_plot_axis(dpg.mvXAxis, label='Вісь X')
                    dpg.add_plot_axis(dpg.mvYAxis, label='Вісь Y', tag='y_axis')

    with dpg.window(label='Нова точка концентрації...', tag='popup', modal=True, show=False, no_close=True):
        
        dpg.add_text('Координати концентрації:')
        dpg.add_input_float(tag='popup_x', width=-1)
        dpg.add_input_float(tag='popup_y', width=-1)

        dpg.add_button(label='Додати',    tag='popup_add',    callback=callbacks.AddConcentrationPoint, width=-1)
        dpg.add_button(label='Скасувати', tag='popup_cancel', callback=lambda: dpg.hide_item('popup'),  width=-1)

    with dpg.window(label='Новий набір концентрації...', tag='popup2', modal=True, show=False, no_close=True):

        dpg.add_text('')
        dpg.add_input_int(tag='popup2_amount', width=-1)
        dpg.add_button(label='Згенерувати', callback=callbacks.GenConcentrationPoints,  width=-1,  tag='popup2_add')
        dpg.add_button(label='Скасувати',   callback=lambda: dpg.hide_item('popup2'),   width=-1)


def StartWindowPayload():
    dpg.create_viewport(title='Visualizer', width=1280, height=720)
    dpg.setup_dearpygui()
    dpg.set_primary_window('main', True)
    dpg.show_viewport()
    dpg.start_dearpygui()


def Finalize():
    dpg.destroy_context()


