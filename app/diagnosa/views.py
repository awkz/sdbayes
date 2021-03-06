from app.utils import int_to_month
from flask import (
    Blueprint,
    flash,
    redirect,
    render_template,
    url_for,
)
from flask_login import current_user, login_required
from sqlalchemy import extract

from app.decorators import admin_required, pasien_required
from app.diagnosa.bayes import (
    getAtribut,
    getC,
    likehood,
)
from app.diagnosa.forms import PrintLaporan
from app.models import Diagnosa, Label, Pasien, Pilihan, Training, User

diagnosa = Blueprint("diagnosa", __name__)


@diagnosa.route("/")
@login_required
@admin_required
def index():
    """Index Diagnosa page."""
    diagnosa = (
        Pasien.query.join(User, Pasien.user == User.id)
        .join(Diagnosa, Pasien.user == Diagnosa.user)
        .add_columns(
            Pasien.id,
            User.first_name.label("first_name"),
            User.last_name.label("last_name"),
            Pasien.k1,
            Pasien.k2,
            Pasien.k3,
            Pasien.k4,
            Pasien.k5,
            Pasien.k6,
            Pasien.k7,
            Diagnosa.tingkatkecemasan,
            Diagnosa.sedikitatautidakada,
            Diagnosa.ringan,
            Diagnosa.sedang,
            Diagnosa.parah,
        )
        .all()
    )
    pilihans = Pilihan.query.all()
    labels = Label.query.all()
    return render_template(
        "diagnosa/index.html",
        diagnosa=diagnosa,
        pilihans=pilihans,
        labels=labels,
    )


@diagnosa.route("/report", methods=["GET", "POST"])
@login_required
@admin_required
def report():
    form = PrintLaporan()
    if form.validate_on_submit():
        bulan = form.bulan.data
        bln, thn = bulan.split("-")
        diagnosa = (
            Pasien.query.join(User, Pasien.user == User.id)
            .join(Diagnosa, Pasien.user == Diagnosa.user)
            .add_columns(
                Pasien.id,
                User.first_name.label("first_name"),
                User.last_name.label("last_name"),
                Pasien.k1,
                Pasien.k2,
                Pasien.k3,
                Pasien.k4,
                Pasien.k5,
                Pasien.k6,
                Pasien.k7,
                Diagnosa.tingkatkecemasan,
                Diagnosa.sedikitatautidakada,
                Diagnosa.ringan,
                Diagnosa.sedang,
                Diagnosa.parah,
                Diagnosa.datetime,
            )
            .filter(
                extract("month", Diagnosa.datetime) == int(bln),
                extract("year", Diagnosa.datetime) == int(thn),
            )
            .all()
        )
        pilihans = Pilihan.query.all()
        labels = Label.query.all()
        return render_template(
            "diagnosa/report.html",
            form=form,
            diagnosa=diagnosa,
            pilihans=pilihans,
            labels=labels,
            bln=int_to_month(int(bln)),
            thn=int(thn),
        )
    return render_template("diagnosa/report.html", form=form)


@diagnosa.route("/detail/<id>", methods=["GET", "POST"])
@login_required
@admin_required
@pasien_required
def detail(id):
    """Detail data diagnosa."""
    trainings = Training.query.all()
    pilihans = Pilihan.query.all()
    labels = Label.query.all()
    diagnosa = (
        Pasien.query.filter_by(id=id)
        .join(User, Pasien.user == User.id)
        .add_columns(
            Pasien.id,
            User.first_name.label("first_name"),
            User.last_name.label("last_name"),
            Pasien.k1,
            Pasien.k2,
            Pasien.k3,
            Pasien.k4,
            Pasien.k5,
            Pasien.k6,
            Pasien.k7,
            Pasien.user,
        )
        .first()
    )
    k1 = getAtribut("k1")
    k2 = getAtribut("k2")
    k3 = getAtribut("k3")
    k4 = getAtribut("k4")
    k5 = getAtribut("k5")
    k6 = getAtribut("k6")
    k7 = getAtribut("k7")
    c = getC()
    lh = likehood(id)
    hasildiagnosa = (
        Diagnosa.query.filter_by(user=diagnosa.user)
        .add_columns(Diagnosa.tingkatkecemasan)
        .first()
    )
    return render_template(
        "diagnosa/detail.html",
        trainings=trainings,
        pilihans=pilihans,
        labels=labels,
        diagnosa=diagnosa,
        k1=k1,
        k2=k2,
        k3=k3,
        k4=k4,
        k5=k5,
        k6=k6,
        k7=k7,
        c=c,
        lh=lh,
        hasildiagnosa=hasildiagnosa,
    )


@diagnosa.route("/pasien/<id>", methods=["GET", "POST"])
@login_required
@pasien_required
def pasien(id):
    if Pasien.query.filter_by(user=id).count() != 0:
        """data diagnosa."""
        trainings = Training.query.all()
        pilihans = Pilihan.query.all()
        labels = Label.query.all()
        diagnosa = (
            Pasien.query.filter_by(user=id)
            .join(User, Pasien.user == User.id)
            .add_columns(
                Pasien.id,
                User.first_name.label("first_name"),
                User.last_name.label("last_name"),
                Pasien.k1,
                Pasien.k2,
                Pasien.k3,
                Pasien.k4,
                Pasien.k5,
                Pasien.k6,
                Pasien.k7,
                Pasien.user,
            )
            .first()
        )
        k1 = getAtribut("k1")
        k2 = getAtribut("k2")
        k3 = getAtribut("k3")
        k4 = getAtribut("k4")
        k5 = getAtribut("k5")
        k6 = getAtribut("k6")
        k7 = getAtribut("k7")
        c = getC()
        lh = likehood(diagnosa.id)
        hasildiagnosa = Diagnosa.query.filter_by(user=diagnosa.user).first()
        return render_template(
            "diagnosa/pasien.html",
            trainings=trainings,
            pilihans=pilihans,
            labels=labels,
            diagnosa=diagnosa,
            k1=k1,
            k2=k2,
            k3=k3,
            k4=k4,
            k5=k5,
            k6=k6,
            k7=k7,
            c=c,
            lh=lh,
            hasildiagnosa=hasildiagnosa,
        )
    else:
        flash("Data pasien {} harus diisi".format(current_user.full_name()), "warning")
        return redirect(url_for("pasien.input"))


@diagnosa.route("/pasien/detail/<id>", methods=["GET", "POST"])
@login_required
@pasien_required
def pasien_detail(id):
    """Detail data diagnosa."""
    trainings = Training.query.all()
    pilihans = Pilihan.query.all()
    labels = Label.query.all()
    diagnosa = (
        Pasien.query.filter_by(id=id)
        .join(User, Pasien.user == User.id)
        .add_columns(
            Pasien.id,
            User.first_name.label("first_name"),
            User.last_name.label("last_name"),
            Pasien.k1,
            Pasien.k2,
            Pasien.k3,
            Pasien.k4,
            Pasien.k5,
            Pasien.k6,
            Pasien.k7,
            Pasien.user,
        )
        .first()
    )
    k1 = getAtribut("k1")
    k2 = getAtribut("k2")
    k3 = getAtribut("k3")
    k4 = getAtribut("k4")
    k5 = getAtribut("k5")
    k6 = getAtribut("k6")
    k7 = getAtribut("k7")
    c = getC()
    lh = likehood(id)
    hasildiagnosa = (
        Diagnosa.query.filter_by(user=diagnosa.user)
        .add_columns(Diagnosa.tingkatkecemasan)
        .first()
    )
    return render_template(
        "diagnosa/detail.html",
        trainings=trainings,
        pilihans=pilihans,
        labels=labels,
        diagnosa=diagnosa,
        k1=k1,
        k2=k2,
        k3=k3,
        k4=k4,
        k5=k5,
        k6=k6,
        k7=k7,
        c=c,
        lh=lh,
        hasildiagnosa=hasildiagnosa,
    )
