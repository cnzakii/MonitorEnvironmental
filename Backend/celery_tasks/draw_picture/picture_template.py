import os
import sys
sys.path.append('../..')
import pyecharts.options as opts
from pyecharts.charts import Line
from pyecharts.commons.utils import JsCode
from lib import config


def draw(x_data, y_data, background, title, y_name, file_name):
    root = config.read_config('other').get('flask_path')
    c = (
        Line(init_opts=opts.InitOpts(
            width='900px',
            height='500px',
            page_title=title,
            bg_color=JsCode(background),
        )
        )
            .add_xaxis(xaxis_data=x_data)
            .add_yaxis(
            series_name="环境监测",
            y_axis=y_data,
            # Smooth curve
            is_smooth=False,
            # Display point
            is_symbol_show=False,
            # Line style configuration item
            linestyle_opts=opts.LineStyleOpts(width=1.5, color="#fff", opacity=0.8),
            label_opts=opts.LabelOpts(is_show=False),
            # 提示框组件配置项
            # Element style configuration item
            tooltip_opts=opts.TooltipOpts(is_show=False),
            # 填充区域配置项
            # Fill area configuration item
            areastyle_opts=opts.AreaStyleOpts(
                opacity=0.15,
                color="#ffffff"
            ),
        )
            .set_global_opts(
            # 标题设置
            # Set title
            title_opts=opts.TitleOpts(
                title=title,
                pos_bottom="92%",
                pos_left="center",
                title_textstyle_opts=opts.TextStyleOpts(color="#fff", font_size=24),
            ),
            # Configure X-axis
            xaxis_opts=opts.AxisOpts(
                # Time axis
                type_="time",
                max_interval=3600 * 24 * 50,
                # Name
                name='Time',
                name_textstyle_opts=opts.TextStyleOpts(color="#fff", font_size=14),
                # Distance between axis name and axis
                name_gap=30,
                # Timeline without edges
                boundary_gap=False,
                # 坐标轴刻度线配置项 数值于X轴距离 颜色
                # Coordinate axis scale line configuration item
                axislabel_opts=opts.LabelOpts(margin=12, color="#fff"),
                # Show X axis
                axisline_opts=opts.AxisLineOpts(
                    is_show=True,
                    linestyle_opts=opts.LineStyleOpts(width=2, color="#fff")
                ),
                # Does not extend beyond the X axis
                axistick_opts=opts.AxisTickOpts(is_show=False),
                # The line perpendicular to the X axis is required
                splitline_opts=opts.SplitLineOpts(
                    is_show=True,
                    linestyle_opts=opts.LineStyleOpts(color="#ffffff1f")
                ),

            ),
            # Configure Y axis
            yaxis_opts=opts.AxisOpts(
                type_="value",
                # Name
                name=y_name,
                name_textstyle_opts=opts.TextStyleOpts(color="#fff", font_size=16),
                # Distance between axis name and axis
                name_gap=30,
                # Y-axis on the right
                position="right",
                # 坐标轴刻度线配置项 数值于X轴距离 颜色
                # Coordinate axis scale line configuration item
                axislabel_opts=opts.LabelOpts(margin=12, color="#fff"),
                # Y-axis tick mark configuration
                axisline_opts=opts.AxisLineOpts(
                    linestyle_opts=opts.LineStyleOpts(width=2, color="#fff")
                ),
                # Line beyond Y-axis
                axistick_opts=opts.AxisTickOpts(
                    is_show=True,
                    length=16,
                    linestyle_opts=opts.LineStyleOpts(color="#ffffff1f"),
                ),
                # Need some line perpendicular to the Y axis
                splitline_opts=opts.SplitLineOpts(
                    is_show=True,
                    linestyle_opts=opts.LineStyleOpts(color="#ffffff1f")
                ),
            ),
            legend_opts=opts.LegendOpts(is_show=False),
        )
            .render(os.path.join(root, file_name))
    )
