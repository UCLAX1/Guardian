import React, { Component } from 'react'
import {connect} from 'react-redux'
import {signIn} from '../../store/authActions'

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
  }
  render() {
    const {authError}=this.props;
    return (
      <div className="container">
        <form className="white" onSubmit={this.Sumbit}>
            <h5 className="grey-text text-darken-3">Sign In</h5>
            <div className="input-field">
                <label htmlFor="email">Email</label>
                <input type="email" id="email" onChange={this.Change}/>
            </div>
            <div className="input-field">
                <label htmlFor="password">Password</label>
                <input type="password" id="password" onChange={this.Change}/>
            </div>
            <div className="input-field">
                <button className="btn pink lighten-1 z-depth-0">Login</button>
                <div className="black-text center">
                {authError ? <p>{authError}</p>:null} 
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
