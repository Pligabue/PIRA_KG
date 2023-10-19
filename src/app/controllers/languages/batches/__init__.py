from flask import Blueprint, request, render_template, url_for, redirect, flash
import shutil

from .....constants import DOCUMENT_DIR, TRIPLE_DIR, GRAPH_DIR, BLABKG_DIR
from ....utils.find_batches import find_batches
from ....forms.batch import BatchForm
from .graphs import bp as graph_bp


bp = Blueprint('batches', __name__, url_prefix='/batches')
bp.register_blueprint(graph_bp)


@bp.route("/")
def index(language):
    batches = find_batches(language)
    return render_template("batches/index.j2", language=language, batches=batches)


@bp.route("/new/")
@bp.post("/new/")
def new(language):
    form = BatchForm(request.form)
    form.language.process_data(language)
    if request.method == "POST" and form.validate():
        return redirect(url_for(".index", language=language))
    return render_template("batches/new.j2", language=language, form=form)


@bp.route("/<batch>/delete/")
def delete(language, batch):
    doc_dir = DOCUMENT_DIR / language / batch
    triple_dir = TRIPLE_DIR / language / batch
    graph_dir = GRAPH_DIR / language / batch
    if graph_dir != BLABKG_DIR:
        shutil.rmtree(doc_dir, ignore_errors=True)
        shutil.rmtree(triple_dir, ignore_errors=True)
        shutil.rmtree(graph_dir, ignore_errors=True)
    else:
        flash("Can't delete the official BlabKG graphs.", "error")
    return redirect(url_for(".index", language=language))


@bp.route("/<batch>/")
def batch(language, batch):
    base_graphs = (GRAPH_DIR / language / batch / "base").glob("*.json")
    clean_graphs = (GRAPH_DIR / language / batch / "clean").glob("*.json")
    return render_template(
        "batches/batch.j2",
        language=language,
        batch=batch,
        base_graphs=base_graphs,
        clean_graphs=clean_graphs,
    )
