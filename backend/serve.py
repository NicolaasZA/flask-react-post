from flask import Flask, request, Response

app = Flask(__name__)


@app.route("/", methods=['POST', 'GET', 'OPTIONS'])
def hello_world():

    styling = 'body { background: silver; } table { width: 400px; margin: 20px auto; background: white; border-radius: 4px; } .tac { text-align: center; color: #777; } .tar { text-align: right; } .tal { text-align: left; } td { padding: 6px; } table tr:nth-child(even) { background: whitesmoke; }'

    # ! Lys alle request parameters
    query_param_html = ""
    for param in request.args.to_dict():
        # param is die naam van die parameter
        value = request.args[param]
        query_param_html += f'<tr><td class="tar">{param}</td><td class="tal">{value}</td></tr>'
    if query_param_html == "":
        query_param_html = '<tr class="tac"><td colspan="2">none</td></tr>'

    # NOTE: Jy kan ook spesifieke parameter kry:
    # request.args.get("query_param_name", default="default value", type=str)

    # ! Get form parameters
    form_data_html = ""
    for param in request.form.keys():
        value = request.form.get(param)
        form_data_html += f'<tr><td class="tar">{param}</td><td class="tal">{value}</td></tr>'
    if form_data_html == "":
        form_data_html = '<tr class="tac"><td colspan="2">none</td></tr>'

    # NOTE: Jy kan ook spesifieke parameter kry:
    # request.form.get("form_param_name", default="default value", type=str)

    # ! JSON body
    jason_html = ""
    jason = request.get_json(silent=True, cache=False)

    # jason is None as die request nie 'n JSON request is nie.
    if jason is not None:  
        # Gaan hier in as request JSON is.
        for param in jason:
            value = jason[param]
            jason_html += f'<tr><td class="tar">{param}</td><td class="tal">{value}</td></tr>'

        # NOTE: Jy kan ook spesifieke parameter kry:
        # if "field_name" in jason:
        # # -> field is beskikbaar as jason[field_name]
        # else:
        # # -> field is nie in JSON nie, gebruik fallback of hanteer

    else:
        jason_html = '<tr class="tac"><td colspan="2">none</td></tr>'

    response = Response(f"""
    <style>{styling}</style>
    <table>
        <tr>
            <th colspan="2">Query Parameters</th>
        </tr>
        {query_param_html}
    </table>
    
    <table>
        <tr>
            <th colspan="2">Form Data</th>
        </tr>
        {form_data_html}
    </table>
    
    <table>
        <tr>
            <th colspan="2">JSON Data</th>
        </tr>
        {jason_html}
    </table>""")

    # Add CORS headers
    response.headers['Access-Control-Allow-Methods'] = 'POST, GET, OPTIONS'
    response.headers['Access-Control-Allow-Headers'] = 'Content-Type'
    response.headers['Access-Control-Allow-Origin'] = '*'

    return response
