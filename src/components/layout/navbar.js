import React from 'react'
import {Link} from 'react-router-dom'
import SignedInLinks from './SignedinLinks'
import SignedOutLinks from './SignedOutLinks'
import {connect} from 'react-redux'


const Navbar =(props)=> {


    var styles = {
        color: 'rgb(167,253,250)', 
        fontSize: '72px',
        position: 'absolute',
        left: '200px',
        top: '15px'
    }
    const {auth}=props;
    const links = auth ? <SignedInLinks /> : <SignedOutLinks />;
    
    
    return (
        <nav className="nav-wrapper darken-" style={{height: '120px'}}>
            <div className="container">
                
                <Link to={'/signin'} className="brand-logo" style={styles} >X1 Guardian</Link>
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