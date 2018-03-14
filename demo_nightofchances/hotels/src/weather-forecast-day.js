import React, { Component } from 'react';
import { Col, Panel } from 'react-bootstrap';
import 'bootstrap/dist/css/bootstrap.min.css';
import moment from 'moment';


class ForecastDay extends Component {


  render() {
console.log("weather day", this.props.dateFrom, ' index ' ,this.props.index )
    return (
          <Panel header={moment(this.props.dateFrom).add(this.props.index, 'days').format('DD.MM.YYYY')}>
            <img src={"https://www.metaweather.com/static/img/weather/" + this.props.data.weather_state_abbr + ".svg"} />
            <p style={{textAlign: 'center', lineHeight: '30px'}}>{this.props.data.weather_state_name}</p>
            Temperature: {parseInt(this.props.data.the_temp,10)}<br />

          </Panel>
    );

  }
}

export default ForecastDay;
