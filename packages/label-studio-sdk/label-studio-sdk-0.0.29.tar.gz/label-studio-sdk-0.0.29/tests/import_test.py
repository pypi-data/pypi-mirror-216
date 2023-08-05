LABEL_STUDIO_URL = 'https://fb-lsdv-5218.dev.heartex.com'
API_KEY = 'aaf73cc7ac1e681212a9919d99e907965a32ff37'

# Import the SDK and the client module
from label_studio_sdk import Client

# Connect to the Label Studio API and check the connection
ls = Client(url=LABEL_STUDIO_URL, api_key=API_KEY)
ls.check_connection()

project = ls.start_project(
    title='Image Project',
    label_config='''
    <View>

      <Header value="Select label and click the image to start"/>
      <Image name="image" value="$image" zoom="true"/>

      <PolygonLabels name="label" toName="image"
                     strokeWidth="3" pointSize="small"
                     opacity="0.9">
        <Label value="Airplane" background="red"/>
        <Label value="Car" background="blue"/>
      </PolygonLabels>

    </View>
    '''
)

project.import_tasks(
    [
        {'image': 'https://data.heartex.net/open-images/train_0/mini/0045dd96bf73936c.jpg'},
        {'image': 'https://data.heartex.net/open-images/train_0/mini/0083d02f6ad18b38.jpg'}
    ]
)
