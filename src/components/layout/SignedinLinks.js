import React from 'react'
import {NavLink} from 'react-router-dom'
import {connect} from 'react-redux'
import {signOut} from '../../store/authActions'


const SignedInLinks=(props)=> {

    return (
        <ul className="right">
            <li><a onClick={props.signOut}><NavLink to ='/signin'>Sign Out</NavLink></a></li>
            <li><NavLink to='/camera'>Feed</NavLink></li>
            
        </ul>
    )
}

const mapDispatchToProps =(dispatch) => {
    return {
        signOut: () => dispatch(signOut())
    }
}
export default connect(null,mapDispatchToProps)(SignedInLinks);