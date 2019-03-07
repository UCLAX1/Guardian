

const initState={
    authError: 'undefined'
}

const authReducer = (state=initState, action) => {
    switch(action.type){
        case 'LOGIN_ERROR':
            console.log('error');
             return {
            ...state,
            authError:'Login failed. Please try again'
             }
        case 'LOGIN_SUCCESS':
             console.log('success');
             
             return {
            ...state,
            authError:null
          
             }
        case 'SIGNOUT_SUCCESS':
             console.log('signout');
             
             return {
                authError:'undefined',
                state
             }
             
        
        default:
             return state;
    }
   
}

export default authReducer;