import React, { createContext, useReducer, useEffect } from 'react';

export const globalContext = createContext();
const initialState = {
    breadcrumb: false
};
const GlobalContextProvider = (props) => {

    const [globalReducer, dispatch] = useReducer(globalReducer, initialState, () => {
        const localData = localStorage.getItem('app');
        return localData ? JSON.parse(localData) : [];
    });

    useEffect(() => {
        localStorage.setItem('app', JSON.stringify(globalReducer));
    }, [globalReducer]);

    return (
        <GlobalContext.Provider value={{ globalReducer, dispatch }}>
            {props.children}
        </GlobalContext.Provider>
    );
}

export default GlobalContextProvider