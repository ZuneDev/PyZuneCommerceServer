from xml.dom.minidom import Document, Element
import xml.dom.minidom as xml

from flask import Flask, request, Response
import musicbrainzngs

from atom.factory import *

from locale import *
locale = getdefaultlocale()[0]


app = Flask(__name__)
musicbrainzngs.set_useragent("Zune", "4.8", "https://github.com/yoshiask/PyZuneCommerceServer")


@app.route(f"/v2/<string:locale>/account/signin", methods=['POST'])
def account_signin(locale: str):
    try:
        print(request.data)
        signinReq: Document = xml.parseString(request.data.decode('utf-8'))
        tunerInfo: Element = signinReq.firstChild
        idElem: Element = tunerInfo.getElementsByTagName("ID")[0]
        nameElem: Element = tunerInfo.getElementsByTagName("Name")[0]
        typeElem: Element = tunerInfo.getElementsByTagName("Type")[0]
        versionElem: Element = tunerInfo.getElementsByTagName("Version")[0]
        id: str = idElem.firstChild.data

        doc: Document = minidom.Document()
        feed: Element = create_feed(doc, "album_name", "album_id", request.endpoint)

        # doc.appendChild(feed)
        xml_str = doc.toprettyxml(indent="\t")
        return Response(xml_str, mimetype=MIME_XML)
    except Exception as e:
        import traceback
        return Response(traceback.format_exc(), status=500, mimetype="text/plain")


if __name__ == "__main__":
    app.run(port=443)
