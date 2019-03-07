import React, { Component } from 'react'



class App extends Component {
  constructor() {
    super();
    
    this.state = {
      showMenu: false,
    };
    
    this.showMenu = this.showMenu.bind(this);
    this.closeMenu = this.closeMenu.bind(this);
  }
  
  showMenu(event) {
    event.preventDefault();
    
    this.setState({ showMenu: true }, () => {
      document.addEventListener('click', this.closeMenu);
    });
  }
  
  closeMenu(event) {
    
    if (!this.dropdownMenu.contains(event.target)) {
      
      this.setState({ showMenu: false }, () => {
        document.removeEventListener('click', this.closeMenu);
      });  
      
    }
  }
  render() {
   
   
    return (
     
     
         <div className="row">
         <button className="col offset-m0" Text style={{height:"756px",width:"1000px"}}>Hi</button>
      
         <button className="col offset-m2" Text style={{height:"40px",width:"200px",fontSize:"32px"}} >Auto Mode</button>
                <div className="row" style={{height:"40px"}}></div>
                <p className="col offset-m2" style={{color:"black",fontSize:"32px"}}>Motion Controls</p>
                <div className="row" style={{height:"40px"}}></div>
                <p className="col offset-m2"style={{color:"black",fontSize:"32px"}}>Head Turn: 
                  <input type="text" style={{width:"80px",textAlign:"center",fontSize:"32px"}}></input> deg
                  <div style={{width:"20px"}}></div>
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
                <button className="col offset-m0" > Right </button>
                <button className="col offset-m0"> Left </button>
              </div>
            )
            : (
              null
            )
        }
                  </p>
                 
                <div className="row"style={{height:"40px"}}></div>
                <p className="col offset-m2"style={{color:"black",fontSize:"32px"}}>Body Turn:
                <input type="text" style={{width:"80px",textAlign:"center",fontSize:"32px"}}></input> deg
                <div style={{width:"20px"}}></div>
                  <button onClick={this.showMenu}>Body Turn Direction</button>
        
        {
          this.state.showMenu
            ? (
              <div
                className="menu"
                ref={(element) => {
                  this.dropdownMenu = element;
                }}
              >
                <button className="col offset-m0" > Right </button>
                <button className="col offset-m0"> Left </button>
              </div>
            )
            : (
              null
            )
        }
                </p> 
              
                <p className="col offset-m2"style={{color:"black",fontSize:"32px"}}>Distance: 
                <input type="text" style={{width:"80px",textAlign:"center",fontSize:"32px"}}></input> cm</p>
                <div className="row"style={{height:"80px"}}></div>
               
                <p className="col offset-m1"style={{color:"black",fontSize:"32px"}}>Movement Angle: 
                <input type="text" style={{width:"80px",textAlign:"center",fontSize:"32px"}}></input> deg
                <div style={{width:"20px"}}></div>
                  <button onClick={this.showMenu}>Movement Angle Direction</button>
        
        {
          this.state.showMenu
            ? (
              <div
                className="menu"
                ref={(element) => {
                  this.dropdownMenu = element;
                }}
              >
                <button className="col offset-m5" > Right </button>
                <button className="col offset-m5"> Left </button>
              </div>
            )
            : (
              null
            )
        }
                </p>
                <div className="row"style={{height:"40px"}}></div>
                <p className="col offset-m0" style={{fontSize:"32px"}}>Image Size: 1000 x 756</p>
                <button  className="col s12 m1 offset-m7" Text style={{height:"40px",width:"200px",fontSize:"32px"}}>Enter</button>
                <div className="row"></div>
                <p className="col offset-m0"style={{fontSize:"32px"}}>Link Position: x, y</p>
                <div className="row"></div>
                <p className="col offset-m0" style={{fontSize:"32px"}}>Laser Positions: x, y</p>
                
            

        </div>
      
    )
  }
}

export default App;
