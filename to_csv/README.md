# Eratos Example Model: to_csv

A contrived example of a Senaps operator that demonstrates downloading observations from the Senaps platform and writes the results as a CSV.

# preparing the model:

 1. check and update the manifest.json to install the model in the desired organisation and group. 
    NOTE: You must have the required permissions for the organisation and group specified.  
 
```json
  {
  "baseImage": "B415DE8D-4886-4E43-B33A-692DB431C99E",
  "organisationId": "<the organisation id the group below belongs to>",
  "groupIds": [
    "<the group id you have permission to install models to>"
  ],
  "entrypoint": "model.py",
  "dependencies": [],
  "models": [
    {
      "id": "<the model id in the model.py (example @model("joeratos.example.to_csv"))>",
      "name": "Eratos Example Model: To CSV",
      "version": "0.0.0",
      "description": "Loads a set of data streams and outputs the results as a csv document",
      "method": "",
      "ports": [
  ...
```

2. check and update `model.py` `@model` annotation to exactly match the `models.id` in the `manifest.json`

```python
@model("eratos.examples.to_csv")
def to_csv(context):
...
```

3. Create a zip archive with the following files:
```
manifest.json
model.py
senaps_utils.py
```

4. Upload the model to Senaps: https://senaps.eratos.com/#/app/model/upload

5. Once the model has been successfully uploaded, a workflow can be created to test the model in Senaps.


TODO: 
1. Provide test code to run outside of Senaps.