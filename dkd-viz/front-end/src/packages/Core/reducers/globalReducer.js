const globalReducer = (state, action) => {
    switch (action.type) {
        case "ADD_BREADCUB":
            return {
                ...state,
                breadcrumb: action.breadcrumb
            };
        default:
            return state;
    }
}

export {
    globalReducer
}