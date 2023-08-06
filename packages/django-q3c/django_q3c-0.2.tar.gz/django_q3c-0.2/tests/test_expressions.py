import pytest

from django.db import connection

from django_q3c import expressions

from q3c_test.models import Position


@pytest.mark.django_db
def test_q3c_version():
    with connection.cursor() as cursor:
        cursor.execute("SELECT q3c_version()")
        postgres_value = cursor.fetchone()[0]

    Position(ra=35, dec=23).save()
    django_value = Position.objects.annotate(
        version=expressions.Q3CVersion()
    ).first().version

    assert django_value == postgres_value


@pytest.mark.django_db
def test_q3c_ang2ipix():
    ra, dec = 12, 14
    with connection.cursor() as cursor:
        cursor.execute(
            "SELECT q3c_ang2ipix(%s, %s)", [ra, dec]
        )
        postgres_value = cursor.fetchone()[0]

    Position(ra=35, dec=23).save()
    django_value = Position.objects.annotate(
        distance=expressions.Q3CAng2IPix(ra_col=ra, dec_col=dec)
    ).first().distance

    assert django_value == postgres_value


@pytest.mark.django_db
def test_q3c_dist():
    ra1, dec1, ra2, dec2 = 12, 14, 13, 15
    with connection.cursor() as cursor:
        cursor.execute(
            "SELECT q3c_dist(%s, %s, %s, %s)", [ra1, dec1, ra2, dec2]
        )
        postgres_value = cursor.fetchone()[0]

    Position(ra=35, dec=23).save()
    django_value = Position.objects.annotate(
        distance=expressions.Q3CDist(ra1=ra1, dec1=dec1, ra2=ra2, dec2=dec2)
    ).first().distance

    assert django_value == postgres_value


@pytest.mark.django_db
def test_q3c_dist_pm():
    ra1, dec1, ra2, dec2 = 12, 14, 13, 15
    pmra1, pmdec1 = 1, 1 #marcsec/yr
    epoch1, epoch2 = 2000, 2010
    cosdec_flag = 1
    with connection.cursor() as cursor:
        cursor.execute(
            "SELECT q3c_dist_pm(%s, %s, %s, %s, %s, %s, %s, %s, %s)",
            [ra1, dec1, pmra1, pmdec1, cosdec_flag, epoch1, ra2, dec2, epoch2]
        )
        postgres_value = cursor.fetchone()[0]

    Position(ra=35, dec=23).save()
    django_value = Position.objects.annotate(
        distance=expressions.Q3CDistPM(
            ra1=ra1, dec1=dec1, pmra1=pmra1, pmdec1=pmdec1,
            cosdec_flag=cosdec_flag, epoch1=epoch1, ra2=ra2, dec2=dec2,
            epoch2=epoch2,
        )
    ).first().distance

    assert django_value == postgres_value


@pytest.mark.django_db
def test_q3c_join():
    ra, dec, ra_col, dec_col = 12, 14, 13, 15
    radius = 2
    with connection.cursor() as cursor:
        cursor.execute(
            "SELECT q3c_join(%s, %s, %s, %s, %s)", [
                ra, dec, ra_col, dec_col, radius,
            ]
        )
        postgres_value = cursor.fetchone()[0]

    Position(ra=35, dec=23).save()
    django_value = Position.objects.annotate(
        distance=expressions.Q3CJoin(
            ra=ra, dec=dec, ra_col=ra_col, dec_col=dec_col, radius=radius,
        )
    ).first().distance

    assert django_value == postgres_value


@pytest.mark.django_db
def test_q3c_join_pm():
    ra, dec, ra_col, dec_col = 12, 14, 13, 15
    radius = 2
    pmra, pmdec = 1, 1 #marcsec/yr
    epoch, epoch_col = 2000, 2010
    max_delta_epoch = 10
    cosdec_flag = 1
    with connection.cursor() as cursor:
        cursor.execute(
            "SELECT q3c_join_pm(%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)", [
                ra, dec, pmra, pmdec, cosdec_flag, epoch, ra_col, dec_col,
                epoch_col, max_delta_epoch, radius,
            ]
        )
        postgres_value = cursor.fetchone()[0]

    Position(ra=35, dec=23).save()
    django_value = Position.objects.annotate(
        distance=expressions.Q3CJoinPM(
            ra=ra, dec=dec, pmra=pmra, pmdec=pmdec, cosdec_flag=cosdec_flag,
            epoch=epoch, ra_col=ra_col, dec_col=dec_col, epoch_col=epoch_col,
            radius=radius, max_delta_epoch=max_delta_epoch,
        )
    ).first().distance

    assert django_value == postgres_value


@pytest.mark.django_db
def test_q3c_ellipse_join():
    ra, dec, ra_col, dec_col = 12, 14, 13, 15
    major_axis, axis_ratio, position_angle = 5, 0.5, 45
    with connection.cursor() as cursor:
        cursor.execute(
            "SELECT q3c_ellipse_join(%s, %s, %s, %s, %s, %s, %s)", [
                ra, dec, ra_col, dec_col, major_axis, axis_ratio, position_angle
            ]
        )
        postgres_value = cursor.fetchone()[0]

    Position(ra=35, dec=23).save()
    django_value = Position.objects.annotate(
        distance=expressions.Q3CEllipseJoin(
            ra=ra, dec=dec, ra_col=ra_col, dec_col=dec_col, major_axis=major_axis,
            axis_ratio=axis_ratio, position_angle=position_angle,
        )
    ).first().distance

    assert django_value == postgres_value


@pytest.mark.django_db
def test_q3c_radial_query():
    center_ra, center_dec, ra_col, dec_col = 12, 14, 13, 15
    radius = 2
    with connection.cursor() as cursor:
        cursor.execute(
            "SELECT q3c_radial_query(%s, %s, %s, %s, %s)", [
                center_ra, center_dec, ra_col, dec_col, radius,
            ]
        )
        postgres_value = cursor.fetchone()[0]

    Position(ra=35, dec=23).save()
    django_value = Position.objects.annotate(
        distance=expressions.Q3CRadialQuery(
            center_ra=center_ra, center_dec=center_dec, ra_col=ra_col,
            dec_col=dec_col, radius=radius,
        )
    ).first().distance

    assert django_value == postgres_value


@pytest.mark.django_db
def test_q3c_ellipse_query():
    center_ra, center_dec, ra_col, dec_col = 12, 14, 13, 15
    major_axis, axis_ratio, position_angle = 5, 0.5, 45
    with connection.cursor() as cursor:
        cursor.execute(
            "SELECT q3c_ellipse_query(%s, %s, %s, %s, %s, %s, %s)", [
                center_ra, center_dec, ra_col, dec_col, major_axis, axis_ratio,
                position_angle
            ]
        )
        postgres_value = cursor.fetchone()[0]

    Position(ra=35, dec=23).save()
    django_value = Position.objects.annotate(
        distance=expressions.Q3CEllipseQuery(
            center_ra=center_ra, center_dec=center_dec, ra_col=ra_col,
            dec_col=dec_col, major_axis=major_axis, axis_ratio=axis_ratio,
            position_angle=position_angle,
        )
    ).first().distance

    assert django_value == postgres_value


@pytest.mark.django_db
def test_q3c_poly_query():
    ra, dec = 12, 14
    polygon = [[10, 10], [10, 15], [15, 15], [15, 10]]
    with connection.cursor() as cursor:
        cursor.execute(
            "SELECT q3c_poly_query(%s, %s, %s)", [ra, dec, polygon]
        )
        postgres_value = cursor.fetchone()[0]

    Position(ra=35, dec=23).save()
    django_value = Position.objects.annotate(
        pos=expressions.Q3CPolyQuery(ra=ra, dec=dec, poly=polygon)
    ).first().pos

    assert django_value == postgres_value


@pytest.mark.django_db
def test_q3c_pixarea():
    ipix = 2059368584689556581
    bits = 10
    with connection.cursor() as cursor:
        cursor.execute(
            "SELECT q3c_pixarea(%s, %s)", [ipix, bits]
        )
        postgres_value = cursor.fetchone()[0]

    Position(ra=35, dec=23).save()
    django_value = Position.objects.annotate(
        pos=expressions.Q3CPixArea(ipix=ipix, bits=bits)
    ).first().pos

    assert django_value == postgres_value


@pytest.mark.django_db
def test_q3c_ipixcenter():
    ra, dec = 12, 14
    bits = 10
    with connection.cursor() as cursor:
        cursor.execute(
            "SELECT q3c_ipixcenter(%s, %s, %s)", [ra, dec, bits]
        )
        postgres_value = cursor.fetchone()[0]

    Position(ra=35, dec=23).save()
    django_value = Position.objects.annotate(
        pos=expressions.Q3CIPixCenter(ra=ra, dec=dec, bits=bits)
    ).first().pos

    assert django_value == postgres_value


@pytest.mark.django_db
def test_q3c_in_poly():
    ra, dec = 12, 14
    polygon = [[10, 10], [10, 15], [15, 15], [15, 10]]
    with connection.cursor() as cursor:
        cursor.execute(
            "SELECT q3c_in_poly(%s, %s, %s)", [ra, dec, polygon]
        )
        postgres_value = cursor.fetchone()[0]

    Position(ra=35, dec=23).save()
    django_value = Position.objects.annotate(
        pos=expressions.Q3CInPoly(ra=ra, dec=dec, poly=polygon)
    ).first().pos

    assert django_value == postgres_value


@pytest.mark.django_db
def test_q3c_ipix2ang():
    ipix = 2059368584689556581
    with connection.cursor() as cursor:
        cursor.execute(
            "SELECT q3c_ipix2ang(%s)", [ipix]
        )
        postgres_value = cursor.fetchone()[0]

    Position(ra=35, dec=23).save()
    django_value = Position.objects.annotate(
        pos=expressions.Q3CIPix2Ang(ipix=ipix)
    ).first().pos

    assert django_value == postgres_value
