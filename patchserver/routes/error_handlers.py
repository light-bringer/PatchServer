from flask import (
    blueprints,
    current_app,
    flash,
    jsonify,
    redirect,
    request,
    url_for
)
from sqlalchemy.exc import IntegrityError

from patchserver.exc import (
    InvalidPatchDefinitionError,
    InvalidWebhook,
    PatchArchiveRestoreFailure,
    SoftwareTitleNotFound,
    Unauthorized
)

blueprint = blueprints.Blueprint('error_handlers', __name__)


@blueprint.app_errorhandler(Unauthorized)
def unauthorized(err):
    current_app.logger.error(str(err))

    if request.args.get('redirect'):
        flash(
            {
                'title': 'Unauthorized',
                'message': str(err)
            },
            'warning')
        return redirect(url_for('web_ui.index'))
    else:
        return jsonify({'unauthorized': str(err)}), 401


@blueprint.app_errorhandler(InvalidPatchDefinitionError)
def error_invalid_patch_definition(err):
    current_app.logger.error(str(err))

    if request.args.get('redirect'):
        flash(
            {
                'title': 'Invalid Patch Definition JSON',
                'message': str(err)
            },
            'warning')
        return redirect(url_for('web_ui.index'))
    else:
        return jsonify({'invalid_json': str(err)}), 400


@blueprint.app_errorhandler(InvalidWebhook)
def error_invalid_webhook(err):
    current_app.logger.error(str(err))

    if request.args.get('redirect'):
        flash(
            {
                'title': 'Invalid Webhook',
                'message': str(err)
            },
            'warning')
        return redirect(url_for('web_ui.index'))
    else:
        return jsonify({'invalid_json': str(err)}), 400


@blueprint.app_errorhandler(SoftwareTitleNotFound)
def error_title_not_found(err):
    current_app.logger.error(err)
    if request.args.get('redirect'):
        flash(
            {
                'title': 'Software title not found',
                'message': str(err)
            },
            'warning')
        return redirect(url_for('web_ui.index'))
    else:
        return jsonify({'title_not_found': str(err)}), 404


@blueprint.app_errorhandler(IntegrityError)
def database_integrity_error(err):
    if 'software_titles.id_name' in str(err):
        message = 'A software title of the given name already exists.'
    else:
        message = str(err)

    if request.args.get('redirect'):
        flash(
            {
                'title': 'There was a conflict',
                'message': message
            },
            'danger')
        return redirect(url_for('web_ui.index'))
    else:
        return jsonify({'database_conflict': message}), 409


@blueprint.app_errorhandler(PatchArchiveRestoreFailure)
def archive_restore_failure(err):
    current_app.logger.error(str(err))

    if request.args.get('redirect'):
        flash(
            {
                'title': 'Unable to Restore Patch Archive',
                'message': str(err)
            },
            'warning')
        return redirect(url_for('web_ui.index'))
    else:
        return jsonify({'restore_failure': str(err)}), 400
