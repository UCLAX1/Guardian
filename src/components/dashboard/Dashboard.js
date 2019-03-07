import React, {Component} from 'react'
import {Redirect} from 'react-router-dom'
import {connect} from 'react-redux'


class Dashboard extends Component {
    render() {
        const {auth}=this.props;
        if (!auth.uid) return <Redirect to='/signin' />
       
        return (
            <div className="dashboard container">
                <div className="row">
                    
                    <div className="col s12 m5 offset-m10">
                    
                    </div>
                   
                </div>
            </div>
        )
    }
}

const mapStateToProps =(state)=>{
    return {
        auth: state.firebase.auth
    }
}

export default connect(mapStateToProps)(Dashboard);