import axios from "axios";
import { useDispatch, useSelector } from "react-redux";

import {
    setReadyState,
    setGeogrid,
    setModule
} from './dataloaderSlice';
import settings from "../../settings/config.json";

const getAPICall = async (URL: string) => {
    try {
        const response = await axios.get(URL);
        return response.data;
    } catch (err) {
        console.log(err);
    }
};

export default function DataLoader(props: any) {
    const { tableName } = props;
    const url = settings.apiURL + '/table/' + tableName;

    const dispatch = useDispatch();

    async function getModules() {
        console.log("Start Fetching: " + url)
        const modules = await getAPICall(url);
        console.log("modules here", modules);
        if (modules) {
            dispatch(setGeogrid('geogrid' in modules ? modules.geogrid : []));
            dispatch(setModule('mod' in modules ? modules.mod : {} ));
        }

        // send to cityio
        console.log("done fetching from cityIO");
    }

    getModules();
    dispatch(setReadyState(true));

    return null;
}
