from app import create_app, db

app = create_app()

from app import routes, models


@app.shell_context_processor
def make_shell_context():
    return {
        'db': db,
        'Candidate': models.Candidate,
        'JobApplication': models.JobApplication,
        'JobAdvertisement': models.JobAdvertisement,
        'Skill': models.Skill,
    }
