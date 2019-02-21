import React from 'react'
import {NavLink} from 'react-router-dom'

const SignedOutLinks=()=> {
    var styles = {
        color: 'rgb(215,98,167)'
      };

    return (
        <ul className="right">
            
            <li><NavLink to='/signin' style={styles}>Sign In</NavLink></li>
            
        </ul>
    )
}

export default SignedOutLinks;