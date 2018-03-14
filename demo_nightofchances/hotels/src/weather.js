import React, { Component } from 'react';
import { Grid, Row, Col, Table, Button, Panel } from 'react-bootstrap';
import 'bootstrap/dist/css/bootstrap.min.css';
import ForecastDay from './weather-forecast-day';
import Loader from 'react-loader';

class Weather extends Component {

  constructor() {
    super();
    this.state = {
      loading: true,
      city: null,
      weather: {
        consolidated_weather: []
      }
    };
  }

  componentWillMount() {
    this.getCity().then((json) => {
      if (!json.length) {
        throw "city not found";
      }
      this.setState({
        city: json[0]
      });
      return this.getWeather(json[0].woeid);
    }).then((json) => {
      this.setState({
        weather: json,
        loading: false
      });
    }).catch((error) => {
      console.error(error);
    });
  }

  getCity() {
    var url = 'http://127.0.0.1:8080/?url=https://www.metaweather.com/api/location/search/?query='+this.props.city;
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
            throw({message: "Weather API failed to return data"});
        }
    })
  }

  getWeather(woeid) {
    console.log("WOEID = ",woeid)
    this.setState({loading: true});
    console.log(this.props);
    var url = 'http://127.0.0.1:8080/?url=https://www.metaweather.com/api/location/'+woeid;
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
            throw({message: "Weather API failed to return data"});
        }
    })
  }


  render() {
  /*  if (this.state.loading && !this.state.weather && !this.state.city) {
      return (<div>Loading weather...</div>);
    } else if (this.state.loading && !this.state.weather && this.state.city) {
      return (<div>Loading weather in {this.state.city.title}...</div>);
    } else {
    */


      return (
          <div className="panel panel-default">
            <div className="panel-heading">Weather forecast in { (this.state.city) ? this.state.city.title : '...' }</div>
            <div className="panel-body" style={{minHeight: '100px'}}>
              <Loader loaded={!this.state.loading}>
                <Row>{
                  this.state.weather.consolidated_weather.map((day,i) => {
                    return <Col md={2}><ForecastDay data={day} dateFrom={this.props.dateFrom} index={i} /></Col>
                  })
                }
                </Row>
              </Loader>
            </div>
          </div>
      );
  //  }
  }
}

export default Weather;
