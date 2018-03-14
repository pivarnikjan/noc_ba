import React, { Component } from 'react';
import { Grid, Row, Col, Table, Button, Panel } from 'react-bootstrap';
import 'bootstrap/dist/css/bootstrap.min.css';
import Loader from 'react-loader';

class Wiki extends Component {
  constructor() {
    super();
    this.state = {
      loading: false,
      data: null,
      wiki: null
    };
  }

  componentWillMount() {
    this.getWiki().then((json) => {
      this.setState({
        wiki: json,
        loading: false
      });
    }).catch((error) => {
      console.error(error);
    });
  }




  getWiki() {
    this.setState({loading: true});
    var url = 'http://127.0.0.1:8080/?url=https%3A%2F%2Fen.wikipedia.org%2Fw%2Fapi.php%3Faction%3Dquery%26titles%3D'+this.props.city+'%26prop%3Drevisions%26format%3Djson%26explaintext%3D%26exsectionformat%3Dplain%26prop%3Dextracts%26exsentences%3D3%26exlimit%3D1';
    var request = new Request(url, {
        method: 'GET',
        credentials: 'include',
        redirect: 'follow',
        mode: 'cors',
        headers: new Headers({'Content-Type': 'application/json'})
    });
    return fetch(request).then((response) => {
        if (response.ok) {
            return response.json();
        } else {
            throw({message: "Wiki API failed to return data"});
        }
    })
  }




  render() {
    // if (this.state.loading && !this.state.wiki) {
    //   return (<div>Loading wiki...</div>);
    // } else {


      var wiki = null;
      if (this.state.wiki) {
        var pages = this.state.wiki.query.pages;
        if (Object.keys(pages) && Object.keys(pages)[0] && pages[Object.keys(pages)[0]]) {
          wiki = pages[Object.keys(pages)[0]].extract;
        }
      }

      return (
        <div className="panel panel-default">
          <div className="panel-heading">Wikipedia.com info about { this.props.city }</div>
          <div className="panel-body" style={{minHeight: '100px'}}>
            <Loader loaded={!this.state.loading}>
              {wiki}
            </Loader>
          </div>
        </div>
      );
//  }
  }
}

export default Wiki;
