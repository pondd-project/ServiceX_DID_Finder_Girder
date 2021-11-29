# ServiceX_DID_Finder_Girder
 Access datasets for ServiceX from [yt Hub](https://girder.hub.yt/)

## Finding datasets

This DID finder is designed to take a collection id (https://girder.hub.yt/#collections) as the did in ServiceX and yields the download url's for any folders found within the collection. If the collection has no folders, the download url for the collection is passed to the ServiceX transformer.

## Build Image

Build the docker image as:

```bash
% docker build -t servicex-did-finder-girder .
```

## Deploying the DID Finder

You'll need to create a k8 deployment file in order to run this DID finder. Here is a sample, built to be part of the `ServiceX` distribution:

```yaml
---
apiVersion: apps/v1
kind: Deployment
metadata:
  name: {{ .Release.Name }}-did-finder-girder
spec:
  replicas: 1
  selector:
    matchLabels:
      app: {{ .Release.Name }}-did-finder-girder
  template:
    metadata:
      labels:
        app: {{ .Release.Name }}-did-finder-girder
    spec:
      containers:
      - name: {{ .Release.Name }}-did-finder-girder
        image: {{ .Values.didFinderGirder.image }}:{{ .Values.didFinderGirder.tag }}
        imagePullPolicy: {{ .Values.didFinderGirder.pullPolicy }}
        env:
          - name: INSTANCE_NAME
            value: {{ .Release.Name }}
        args:
          - --rabbit-uri
          - amqp://user:{{ .Values.rabbitmq.auth.password }}@{{ .Release.Name }}-rabbitmq:5672
```

The last argument to `--rabbit-uri` is perhaps the most crucial - it defines the rabbit queue this DID finder listens on.

## Testing Locally

Once deployed locally, you can test the DID Finder by runnign the following command within the tests directory:

```
python3 post.py ${servicex_port} yt.json
```

You will see the urls being returned from the did finder in logs of the did finder container.

