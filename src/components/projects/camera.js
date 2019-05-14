import React, { Component } from 'react'




class App extends Component {
  constructor() {
    super();
    
    this.state = {
      showMenu: false,
      showMenu2: false,
      showMenu3: false,
      AutoMode: false,
      HeadTurn: 'Right',
      HeadDegree: 0,
      BodyDegree: 0,
      MovementDegree: 0,
      RealHead: 0,
      RealBody: 0,
      RealMovement: 0,
      BodyTurn: 'Right',
      Movement: 'Right'
    };
    
    this.showMenu = this.showMenu.bind(this);
    this.showMenu2 = this.showMenu2.bind(this);
    this.showMenu3 = this.showMenu3.bind(this);
    this.closeMenu = this.closeMenu.bind(this);
  }

  ChangeAutoMode = () => {
    this.setState({AutoMode: true});
  }
  ChangeAutoModeFalse = () => {
    this.setState({AutoMode: false});
  }
  ChangeHeadTurnRight = () =>{
    this.setState({HeadTurn: 'Right'});
  }
  ChangeHeadTurnLeft = () => {
    this.setState({HeadTurn: 'Left'});
  }

  handleHead = (e) => {
    this.setState({HeadDegree: e.target.value});
  
  }

  ChangeBodyTurnLeft = () =>{
    this.setState({BodyTurn: 'Left'});
  }
  ChangeBodyTurnRight = () =>{
    this.setState({BodyTurn: 'Right'});
  }

  handleBody = (e) =>{
    this.setState({BodyDegree: e.target.value});
  }

  handleMovement = (e) =>{
    this.setState({MovementDegree:e.target.value});
  }
  ChangeMovementLeft = () =>{
    this.setState({Movement: 'Left'});
  }
  ChangeMovementRight = () =>{
    this.setState({Movement: 'Right'});
  }
  handleall = () =>{
    this.setState({RealHead: this.state.HeadDegree, RealBody: this.state.BodyDegree, RealMovement: this.state.MovementDegree});
    
  }
  showMenu(event) {
    event.preventDefault();
    
    this.setState({ showMenu: true }, () => {
      document.addEventListener('click', this.closeMenu);
    });
    
  }
  showMenu2(event) {
    event.preventDefault();
    
    this.setState({ showMenu2: true }, () => {
      document.addEventListener('click', this.closeMenu);
    });
  }
  showMenu3(event) {
    event.preventDefault();
    
    this.setState({ showMenu3: true }, () => {
      document.addEventListener('click', this.closeMenu);
    });
  }
  
 
  closeMenu(event) {
    
    if (!this.dropdownMenu.contains(event.target)) {
      
      this.setState({ showMenu: false, showMenu2: false, showMenu3: false }, () => {
        document.removeEventListener('click', this.closeMenu);
      });  
      
    }
  }
  render() {
   
   
    return (
    
     
         <div className="row">
         <button className="col offset-m0" Text style={{height:"756px",width:"1000px"}}>Hi</button>
      
         <button className="col offset-m1" Text style={{height:"40px",width:"200px",fontSize:"32px",position:"absolute",right:'300px'}} 
         onClick ={this.ChangeAutoMode}>Auto Mode</button>
         <button Text style={{height:"40px",width:"200px",fontSize:"32px",position:"absolute",right:'100px'}} 
         onClick ={this.ChangeAutoModeFalse}> Cancel</button>
                <div className="row" style={{height:"40px"}}></div>
                
                <p className="col offset-m" style={{color:"black",fontSize:"32px",position:"absolute",right: '200px'}}>Motion Controls</p>
                <div className="row" style={{height:"60px"}}></div>
                <p className="col offset-m2"style={{color:"black",fontSize:"32px",position:"absolute",right:'200px'}}>Head Turn: 
                  <input type="text" style={{width:"80px",textAlign:"center",fontSize:"32px"}} onChange ={this.handleHead}></input> deg
                  <div style={{height:"20px"}}></div>
                  
                  <button onClick={this.showMenu}>Head Turn Direction</button>
        {
          this.state.showMenu
            ? (
              <div
                className="menu"
                ref={(element) => {
                  this.dropdownMenu = element;
                }}
              >
                <button className="col offset-m0" onClick ={this.ChangeHeadTurnRight}> Right </button>
                <button className="col offset-m0" onClick ={this.ChangeHeadTurnLeft}> Left </button>
              </div>
              
            )
            : (
              null
            )
        }
                  </p>
                 
                <div className="row"style={{height:"150px"}}></div>
                <p className="col offset-m2"style={{color:"black",fontSize:"32px",position:'absolute',right:'200px'}}>Body Turn:
                <input type="text" style={{width:"80px",textAlign:"center",fontSize:"32px"}} 
                onChange = {this.handleBody}></input> deg
                <div style={{height:"20px"}}></div>
                  <button onClick={this.showMenu2}>Body Turn Direction</button>
        
        {
          this.state.showMenu2
            ? (
              <div
                className="menu"
                ref={(element) => {
                  this.dropdownMenu = element;
                }}
              >
                <button className="col offset-m0" onClick ={this.ChangeBodyTurnRight}> Right </button>
                <button className="col offset-m0" onClick ={this.changeBodyTurnLeft}> Left </button>
              </div>
            )
            : (
              null
            )
        }
                </p> 
               <div className="row" style={{height:'150px'}} />
                <p className="col offset-m2"style={{color:"black",fontSize:"32px",position:'absolute',right:'200px'}}>Distance: 
                <input type="text" style={{width:"80px",textAlign:"center",fontSize:"32px"}}></input> cm</p>
                <div className="row"style={{height:"80px"}}></div>
               
                <p className="col offset-m2"style={{color:"black",fontSize:"32px",position:'absolute',right:'200px'}}>Movement Angle: 
                <input type="text" style={{width:"80px",textAlign:"center",fontSize:"32px"}}
                onChange = {this.handleMovement}></input> deg
                <div className="row" style={{height:"30px"}}></div>
                  <button onClick={this.showMenu3}>Movement Angle Direction</button>
        
        {
          this.state.showMenu3
            ? (
              <div
                className="menu"
                ref={(element) => {
                  this.dropdownMenu = element;
                }}
              >
                <button className="col offset-m0" onClick ={this.ChangeMovementRight}> Right </button>
                <button className="col offset-m0" onClick ={this.ChangeMovementLeft}> Left </button>
              </div>
            )
            : (
              null
            )
        }
                </p>
                
                <div className="row"style={{height:"60px"}}></div>
                <button Text style={{height:"40px",width:"200px",fontSize:"32px", position:'absolute', top: '950px',right:'200px'}}
                onClick = {this.handleall}>Enter</button>
                <p style={{fontSize:"32px", position:'absolute', top: '900px', left: '20px'}}>Image Size: 1000 x 756</p>
                
              
                <p style={{fontSize:"32px",position:'absolute', top: '950px', left:'20px'}}>Link Position: x, y</p>
                
                <p style={{fontSize:"32px",position:'absolute', top: '1000px', left:'20px'}}>Laser Positions: x, y</p>
                
            

        </div>
      
    )
  }
}

export default App;
