import React, { Component } from 'react';
import { Grid, Row, Col, Table, Button, Panel, NavItem, Nav } from 'react-bootstrap';

class POI extends Component {


  constructor() {
    super();
    this.state = {
      data: [],
      type: 'attraction'
    };
  }

  componentDidMount() {
    this.fetchData(this.state.type);
  }




  getData(type) {
    this.setState({loading: true});
    var url = 'http://local.att.com:8080/?url=http%3A%2F%2Ftour-pedia.org%2Fapi%2FgetPlaces%3Flocation%3D'+this.props.city+'%26category%3D'+type;
    var request = new Request(url, {
        method: 'GET',
        credentials: 'include',
        redirect: 'follow',
        mode: 'cors',
        headers: new Headers({'Content-Type': 'application/json'})
    });
    return fetch(request).then((response) => {
        if (response.ok) {
          this.setState({loading: false});
          return response.json();
        } else {
            throw({message: "POI API failed to return data"});
        }
    })
  }

  handleSelectTab(value) {
    this.setState({type: value}, () => {
      this.fetchData(this.state.type);
    });

  }


  fetchData(type) {
    this.getData(type).then((json) => {
      this.setState({data: json})
    }).catch((error) => {
      console.error(error);
    });
  }

  render() {
    var render = this.state.data.map((item) => {
      return <div>{item.name}</div>
    })



    return (
      <div>
        <Nav bsStyle="tabs" activeKey={this.state.type} onSelect={this.handleSelectTab.bind(this)}>
          <NavItem eventKey="attraction">Attraction</NavItem>
          <NavItem eventKey="restaurant">Restaurant</NavItem>
          <NavItem eventKey="poi">POI</NavItem>
        </Nav>
        <div className="custom-box">
          {render}
        </div>
      </div>
    );

  }
}

export default POI;
