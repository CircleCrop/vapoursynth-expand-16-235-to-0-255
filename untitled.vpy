from vapoursynth import core
from fvsfunc import Depth
core.max_cache_size = 12000
src = core.lsmas.LWLibavSource(r"pre.mp4")
 
# 转换YUV420P8,bt601到RGB24
import vapoursynth as vs
rgb_clip = core.resize.Bicubic(src, format=vs.RGB24, matrix_in_s="470bg", transfer_in_s="601", primaries_in_s="170m", range_in_s="limited")
 
# RGB16~235到0~255的线性拉升
def rescale_value(value):
    return (value - 16) * 255 / (235 - 16)
 
expr = "x {0} - {1} * {2} /".format(16, 255, (235 - 16))
 
# 处理拉升
rescaled_clip = core.std.Expr(rgb_clip, [expr, expr, expr])
 
# 转回YUV空间
output_clip = core.resize.Bicubic(rescaled_clip, format=vs.YUV420P8, matrix_s="709", transfer_s="709", primaries_s="709", range_s="full")
 
out.set_output()
