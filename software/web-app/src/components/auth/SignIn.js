import React, { Component } from 'react'
import {connect} from 'react-redux'
import {signIn} from '../../store/authActions'

class SignIn extends Component {
  constructor(props) {
    super(props);
    this.state={
        email:'',
        password:''
    }
  }

  Change =(e) => {
      this.setState({
          [e.target.id]:e.target.value
      })
  }

  Submit = (e) => {
      e.preventDefault();
      this.props.signIn(this.state);
  }

  render() {
    const {authError}=this.props;
    var styles = {
        color: 'rgb(92,120,142)'
      };
    return (
      <div className="container signin-wrapper">
        <form className="signin-box" onSubmit={this.Submit}>
            <h5 className="signin-text text-darken-3">Sign In</h5>
            <div className="input-field signin-input">
                <label htmlFor="email" style={styles}>Email</label>
                <input type="email" id="email" onChange={this.Change}/>
            </div>
            <div className="input-field signin-input">
                <label htmlFor="password" style={styles}>Password</label>
                <input type="password" id="password" onChange={this.Change} />
            </div>
            <div className="input-field">
                <button className="btn signin-button lighten-1 z-depth-0">Login</button>
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
        authError: state.auth.authError
    }
}
const mapDispatchToProps =(dispatch) => {
    return {
        signIn: (creds) => dispatch(signIn(creds))
    }
}
export default connect(mapStateToProps, mapDispatchToProps)(SignIn);
