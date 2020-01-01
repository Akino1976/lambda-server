
import connexion

app = connexion.App(__name__)
app.add_api('api-specification.yaml', validate_responses=True)

app.run(host='0.0.0.0', port=80, threaded=True)

application = app.app
