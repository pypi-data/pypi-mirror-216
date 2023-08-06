from django.contrib.postgres.fields.array import ArrayField
from django.db.models import fields
from django.db.models.expressions import Func
from django.utils.functional import cached_property


def check_bits(bits):
    if bits > 30 or bits < 1:
        raise ValueError("bits out of range")
    return bits


class Q3CVersion(Func):
    function = "q3c_version"
    arity = 0
    output_field = fields.CharField()


class Q3CAng2IPix(Func):
    function = "q3c_ang2ipix"

    def __init__(self, *, ra_col, dec_col):
        super().__init__(ra_col, dec_col)


class Q3CDist(Func):
    function = "q3c_dist"
    output_field = fields.FloatField()

    def __init__(self, *, ra1, dec1, ra2, dec2):
        super().__init__(ra1, dec1, ra2, dec2)


class Q3CDistPM(Func):
    function = "q3c_dist_pm"
    output_field = fields.FloatField()

    def __init__(
        self, *, ra1, dec1, pmra1, pmdec1, cosdec_flag, epoch1, ra2, dec2,
        epoch2
    ):
        super().__init__(
            ra1, dec1, pmra1, pmdec1, cosdec_flag, epoch1, ra2, dec2, epoch2,
        )


class Q3CJoin(Func):
    function = "q3c_join"
    output_field = fields.BooleanField()

    def __init__(self, *, ra, dec, ra_col, dec_col, radius, ):
        super().__init__(ra, dec, ra_col, dec_col, radius, )


class Q3CJoinPM(Func):
    function = "q3c_join_pm"
    output_field = fields.BooleanField()

    def __init__(
        self, *, ra, dec, pmra, pmdec, cosdec_flag, epoch, ra_col, dec_col,
        epoch_col, max_delta_epoch, radius,
    ):
        super().__init__(
            ra, dec, pmra, pmdec, cosdec_flag, epoch, ra_col, dec_col,
            epoch_col, max_delta_epoch, radius,
        )


class Q3CEllipseJoin(Func):
    function = "q3c_ellipse_join"
    output_field = fields.BooleanField()

    def __init__(
        self, *, ra, dec, ra_col, dec_col, major_axis, axis_ratio,
        position_angle
    ):
        super().__init__(
            ra, dec, ra_col, dec_col, major_axis, axis_ratio, position_angle,
        )


class Q3CRadialQuery(Func):
    function = "q3c_radial_query"
    output_field = fields.BooleanField()

    def __init__(self, *, ra_col, dec_col, center_ra, center_dec, radius):
        super().__init__(ra_col, dec_col, center_ra, center_dec, radius)


class Q3CEllipseQuery(Func):
    function = "q3c_ellipse_query"
    output_field = fields.BooleanField()

    def __init__(
        self, *, ra_col, dec_col, center_ra, center_dec, major_axis,
        axis_ratio, position_angle,
    ):
        super().__init__(
            ra_col, dec_col, center_ra, center_dec, major_axis, axis_ratio,
            position_angle,
        )


class Q3CPolyQuery(Func):
    function = "q3c_poly_query"
    output_field = fields.BooleanField()

    def __init__(self, *, ra, dec, poly):
        super().__init__(ra, dec, poly)


class Q3CPixArea(Func):
    function = "q3c_pixarea"
    output_field = fields.FloatField()

    def __init__(self, *, ipix, bits):
        super().__init__(ipix, check_bits(bits))


class Q3CIPixCenter(Func):
    function = "q3c_ipixcenter"

    def __init__(self, *, ra, dec, bits, ):
        super().__init__(ra, dec, check_bits(bits))


class Q3CInPoly(Func):
    function = "q3c_in_poly"
    output_field = fields.BooleanField()

    def __init__(self, *, ra, dec, poly):
        super().__init__(ra, dec, poly)


class Q3CIPix2Ang(Func):
    function = "q3c_ipix2ang"

    def __init__(self, *, ipix):
        super().__init__(ipix)

    @cached_property
    def output_field(self):
        return ArrayField(fields.FloatField, size=2)
