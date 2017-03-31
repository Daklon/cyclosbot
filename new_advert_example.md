curl -X POST --header 'Content-Type: application/json' --header 'Accept: text/plain' --header 'Authorization: Basic ZGVtbzoxMjM0' -d '{
  "name": "nombre",
  "description": "desc",
  "publicationPeriod": {
    "begin": "2017-03-31T22:35:15.304Z",
    "end": "2018-03-30T22:35:15.304Z"
  },
  "categories": [
      "7762070814178002239"
  ],
  "currency": "7762070814178012479",
  "price": "10",
  "promotionalPrice": "10",
  "promotionalPeriod": {
    "begin": "2017-03-31T22:35:15.304Z",
    "end": "2017-03-31T22:35:15.304Z"
  },
  "customValues": {},
  "addresses": [
    "adress"
  ],
  "kind": "simple",
  "submitForAuthorization": true,
  "hidden": true,
  "images": [
    "string"
  ]
}' 'https://demo.cyclos.org/api/'self'/marketplace'
