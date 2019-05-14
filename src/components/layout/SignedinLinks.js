import React from 'react'
import {connect} from 'react-redux'
import {signOut} from '../../store/authActions'
import {Redirect} from 'react-router-dom'
import {Link} from 'react-router-dom'
import { auth } from 'firebase';
import {SignedOutLinks} from '../layout/SignedOutLinks'

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
           <Link to ='/signin' style={styles} onClick ={<Redirect to = '/signin' />  } >
            
            Login Page</Link>
            
        </ul>
    )
}

const mapDispatchToProps =(dispatch) => {
    return {
        signOut: () => dispatch(signOut())
    }
}
export default connect(null,mapDispatchToProps)(SignedInLinks);