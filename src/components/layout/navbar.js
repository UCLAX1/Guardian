import React from 'react'
import {Link} from 'react-router-dom'
import SignedInLinks from './SignedinLinks'
import SignedOutLinks from './SignedOutLinks'
import {connect} from 'react-redux'


const Navbar =(props)=> {
    const {auth}=props;
    const links=auth.uid ? <SignedInLinks /> : <SignedOutLinks />;
    return (
        <nav className="nav-wrapper red darken-3">
            <div className="container">
                <Link to='/' className="brand-logo">Raspberry Pi Data</Link>
                {links}
                
            </div>
        </nav>
    )
}

const mapStateToProps=(state)=> {
    
    return {
        auth: state.firebase.auth
    }
}

export default connect(mapStateToProps)(Navbar);