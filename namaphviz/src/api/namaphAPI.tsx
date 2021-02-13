import config from '../settings/config.json'

let URL = config['apiURL']

let APIList = {
  Tables: `${URL}/tables`,
  Table: `${URL}/table`,
  Module: `${URL}/sim`
}

function Namaphio() {
  return {
    GetTable: (table: string, field: string = "") => {
      fetch(APIList.Table + `/${table}?field=${field}`)
    }
  }
}

export default Namaphio
