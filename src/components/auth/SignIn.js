import React, { Component } from 'react'
import {connect} from 'react-redux'
import {signIn} from '../../store/authActions'
import {Redirect} from 'react-router-dom'


class SignIn extends Component {
  state={
    email:'',
    password:''
  }
  Change =(e) => {
      this.setState({
          [e.target.id]:e.target.value
      })
  }
  Sumbit = (e) => {
      e.preventDefault();
      this.props.signIn(this.state);
    
      //somehow redirect to feed
  }
  render() {
    const {authError}=this.props;
    return (
         
      <div className="container signin-wrapper" style={{width:'2000px'}}>
        <form className="signin-box" onSubmit={this.Sumbit}>
            <h5 className="signin-text text-lighten-3"style={{fontSize:'48px'}}>Sign In</h5>
            <div className="input-field signin-input" style={{padding: '20px'}}>
                <label htmlFor="email" style={{color:'navy', fontSize:'28px'}}>Email</label>
                <input type="email" id="email" onChange={this.Change}/>
            </div>
            <div className="input-field signin-input" style={{padding:'20px'}}>
                <label htmlFor="password" style={{color:'navy', fontSize:'28px'}}>Password</label>
                <input type="password" id="password" onChange={this.Change}/>
            </div>
            <div className="input-field">
                <button className="btn signin-button lighten-1 z-depth-0" Text style={{fontSize: '32px',width:'620px', height:'80px'}
                } >Login</button>
                <div className="black-text center">
               
                {authError ? <p style={{fontSize:'32px'}}>{authError}</p>:<Redirect to='/camera'/>} 
                
                
    
                
                </div>
            </div>
        </form>
      </div>
    )
  }
}

const mapStateToProps = (state) => {
    return {
        authError:state.auth.authError
    }
}
const mapDispatchToProps =(dispatch) => {
    return {
        signIn: (creds) => dispatch(signIn(creds))
    }
}
export default connect(mapStateToProps, mapDispatchToProps)(SignIn);
