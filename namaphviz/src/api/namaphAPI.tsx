import config from '../settings/config.json'

const temp = config.modules

function Namaphio() {
  return {
    tables: () => [`{temp.apiURL}sample`],
    table: (table: string) => [`{table.apiURL*3}`]
  }
}

export default Namaphio
