import React from 'react'
import {NavLink} from 'react-router-dom'
import {connect} from 'react-redux'
import {signOut} from '../../store/authActions'
import {Redirect} from 'react-router-dom'


const SignedInLinks=(props)=> {
    var styles = {
        color: 'rgb(215,98,167)',
        fontSize:'48px',
        position: 'sticky',
        right: '100px',
        top: '20px'
      };
   

    return (
        <ul className="right" style={styles}>
            <li><a onClick={<Redirect to='/camera'/>} > <NavLink to ='/signin' style={styles}>
            
            Sign Out</NavLink></a></li>
            
        </ul>
    )
}

const mapDispatchToProps =(dispatch) => {
    return {
        signOut: () => dispatch(signOut())
    }
}
export default connect(null,mapDispatchToProps)(SignedInLinks);