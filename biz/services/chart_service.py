# -*- coding:utf-8 -*-

import io
import numpy as np
import matplotlib

matplotlib.use('Agg')
from matplotlib.pylab import plt
from matplotlib.font_manager import FontProperties
from django.conf import settings


# radar chart
def make_radar(skill: int, strength: int, defence: int, willpower: int, attack: int, stamina: int):
    '''
    :return: PNG type image binary content
    '''
    value = [skill, strength, defence, willpower, attack, stamina]
    if not all(map(lambda x: isinstance(x, int) and 0 < x <= 100, value)):
        return
    font = FontProperties(fname=settings.PINGFANG_FONT, size=23)
    plt.figure(figsize=(4.8, 4.8))  # 图片大小
    name = ['技术\n ', '力量       ', '防守       ', '\n意志力', '       进攻 ', '       耐力 ']  # 标签
    theta = np.linspace(0, 2 * np.pi, len(name), endpoint=False)  # 将圆周根据标签的个数等比分
    theta = np.concatenate((theta, [theta[0]]))  # 闭合
    value = np.concatenate((value, [value[0]]))  # 闭合
    ax = plt.subplot(111, projection='polar')  # 构建图例
    ax.set_theta_zero_location('N')  # 设置极轴方向
    ax.fill(theta, value, color="#EF2D55", alpha=0.35)  # 填充色,透明度
    for i in [20, 40, 60, 80, 100]:  # 绘等分线
        ax.plot(theta, [i] * (6 + 1), 'k-', lw=1, color='#8989A3')  # 之所以 n +1，是因为要闭合！
    ax.plot(theta, value, 'ro-', 'k-', lw=1, alpha=0.75, color='#FF465C')  # 绘数据图
    ax.set_thetagrids(theta * 180 / np.pi, name, fontproperties=font, color='#8989A3')  # 替换标签
    ax.set_ylim(0, 100)  # 设置极轴的区间
    ax.spines['polar'].set_visible(False)  # 去掉最外围的黑圈
    ax.grid(True, color='#8989A3', linestyle='-', linewidth=1)
    ax.set_yticks([])
    buf = io.BytesIO()
    plt.savefig(buf, transparent=True)  # 透明
    plt.close('all')  # 关闭所有绘图
    buf.seek(0)
    return buf
