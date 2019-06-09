import React from 'react'
import {Link} from 'react-router-dom'
import SignedInLinks from './SignedinLinks'
import SignedOutLinks from './SignedOutLinks'
import {connect} from 'react-redux'


const Navbar =(props)=> {
    const {auth}=props;
    const links=auth.uid ? <SignedInLinks /> : <SignedOutLinks />;
    const home=auth.uid ? '/camera' : '/'; 
    return (
        <nav className="nav-wrapper darken-3">
            <div className="container">
                <Link to={home} className="brand-logo" style={{color: 'rgb(167,253,250)'}}>X1 Guardian</Link>
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