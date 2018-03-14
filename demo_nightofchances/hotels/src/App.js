import React, { Component } from 'react';
import { Grid, Row, Col, Table, Button, Panel } from 'react-bootstrap';
import DatePicker from 'react-datepicker';
import moment from 'moment';
import Weather from './weather';
import Wiki from './wiki';
import Hotels from './hotels';
import POI from './poi';
import 'bootstrap/dist/css/bootstrap.min.css';
import 'react-datepicker/dist/react-datepicker.css';

class App extends Component {


  constructor() {
    super();
    this.state = {
      city: null,
      dateFrom: moment(),
      dateTo: moment(),
      loading: false
    };
  }


  handleChange(what,value) {
    this.setState({[what]: value});
  }

  handleSubmit(e) {
    e.preventDefault();
    this.setState({loading: false}, () => {
      this.setState({loading: true});
    });
  }


  render() {
    var results = null;
    if (this.state.loading) {
      results = <Grid style={{paddingTop: '10px'}}>
        <Row>
          <Col md={12}>
            <Hotels city={this.state.city} dateFrom={this.state.dateFrom} dateTo={this.state.dateTo} />
          </Col>
        </Row>
        <Row>
          <Col md={12}><Wiki city={this.state.city} /></Col>
        </Row>
        <Row>
          <Col md={12}><Weather city={this.state.city} dateFrom={this.state.dateFrom} /></Col>
        </Row>
        {/*<Row>
          <Col md={12}><POI city={this.state.city} /></Col>
        </Row>*/}

      </Grid>;
    }


    return (
      <Grid style={{paddingTop: '10px'}}>
        <Row>
          <Col md={4}></Col>
          <Col md={4}>
            <Panel>
              <form onSubmit={this.handleSubmit.bind(this)}>
                <Row style={{height: '40px'}}>
                  <Col md={3}>Mesto</Col>
                  <Col md={9}><input type="text" onChange={(e) => {this.handleChange('city', e.target.value)}} value={this.state.city} /></Col>
                </Row>
                <Row style={{height: '40px'}}>
                  <Col md={3}>Od</Col>
                  <Col md={9}><DatePicker
                    selected={this.state.dateFrom}
                    onChange={(value) => {this.handleChange('dateFrom', value)}}
                    dateFormat="DD/MM/YYYY" /></Col>
                </Row>
                <Row style={{height: '40px'}}>
                  <Col md={3}>Do</Col>
                  <Col md={9}><DatePicker
                  selected={this.state.dateTo}
                  onChange={(value) => {this.handleChange('dateTo', value)}}
                  dateFormat="DD/MM/YYYY" /></Col>
                </Row>

                <Row style={{height: '40px'}}>
                  <Col md={3}></Col>
                  <Col md={9}><input type="submit" className="primary" value="Get hotels" /></Col>
                </Row>
              </form>
            </Panel>
          </Col>
          <Col md={4}></Col>
        </Row>
          {results}
      </Grid>

    );


  }
}

export default App;
