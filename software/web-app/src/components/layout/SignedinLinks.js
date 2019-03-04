import React from 'react'
import {NavLink} from 'react-router-dom'
import {connect} from 'react-redux'
import {signOut} from '../../store/authActions'


const SignedInLinks=(props)=> {
    var styles = {
        color: 'rgb(215,98,167)'
      };

    return (
        <ul className="right" style={styles}>
            <li><a onClick={props.signOut}><NavLink to ='/signin' style={styles}>Sign Out</NavLink></a></li>
            <li><NavLink to='/camera' style={styles}>Feed</NavLink></li>
            
        </ul>
    )
}

const mapDispatchToProps =(dispatch) => {
    return {
        signOut: () => dispatch(signOut())
    }
}
export default connect(null,mapDispatchToProps)(SignedInLinks);