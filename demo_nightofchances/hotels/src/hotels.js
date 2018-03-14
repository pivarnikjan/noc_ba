import React, { Component } from 'react';
import { Grid, Row, Col, Table, Button, Panel } from 'react-bootstrap';
import moment from 'moment';
import Wiki from './wiki';
import Loader from 'react-loader';

class Hotels extends Component {


  constructor() {
    super();
    this.state = {
      hotels: null,
      selectedHotelId: null,
      loading: false
    };
  }

  componentDidMount() {
    console.log("city = ",this.props);
    this.setState({loading: true});
    this.fetchHotels(this.props.city, moment(this.props.dateFrom).format("YYYY-MM-DD"), moment(this.props.dateTo).format("YYYY-MM-DD")).then(() => {
      this.getHotels(this.props.city);
      this.setState({loading: false});
        });

  }

  fetchHotels(city,check_in,check_out) {
    var url = 'http://127.0.0.1:8000/v1/hotels';
    var request = new Request(url, {
        method: 'POST',
    //    credentials: 'include',
        redirect: 'follow',
        headers: new Headers({'Content-Type': 'application/json'}),
        body: JSON.stringify({
          city, check_in, check_out
        })
    });
    return fetch(request).then((response) => {
        if (response.ok) {
            if (this.debug)
                console.log("Data received");
            return response.json();
        } else {
            throw({message: "MRS columns API failed to return data"});
        }
    }).then((data) => {
      console.log(data);
      if (data.code !== 2000) {
        return Promise.reject();
      }
      return Promise.resolve();
    });
  }

  getHotels(city) {
    var url = 'http://127.0.0.1:8000/v1/hotels/'+city+'?format=json';
    var request = new Request(url, {
        method: 'GET',
        credentials: 'include',
        redirect: 'follow',
        headers: new Headers({'Content-Type': 'application/json'})
    });
    return fetch(request).then((response) => {
        if (response.ok) {
            if (this.debug)
                console.log("Data received");
            return response.json();
        } else {
            throw({message: "MRS columns API failed to return data"});
        }
    }).then((data) => {
      this.setState({hotels: data})

    });
  }

  handleBack() {
    this.setState({hotels: null});
  }

  handleChange(what,value) {
    this.setState({[what]: value});
  }



  handleShowImage(hotelId) {
    this.setState({selectedHotelId: hotelId});
  }

  render() {
      if (!this.state.loading && this.state.hotels) {
        var rows = this.state.hotels.map((hotel) => {
          return (<tr>
            <td>{hotel.name}</td>
            <td>{hotel.address}</td>
            <td>{hotel.locality}</td>
            <td>{hotel.postal_code}</td>
            <td>{hotel.rating}</td>
            <td>{hotel.price}</td>
            <td><a onClick={this.handleShowImage.bind(this,hotel.id)}>show</a></td>
          </tr>)
        })
      }

      var selectedHotel = null;
      //console.log("this.state.selectedHotelId", this.state.selectedHotelId);
      if (this.state.selectedHotelId) {
        selectedHotel = <div className="panel panel-default"><div className="panel-heading">Hotel image</div><div className="panel-body" style={{padding: '3px'}}><img alt="hotel" src={this.state.hotels.find((hotel) => {
        //  console.log(hotel);
          return this.state.selectedHotelId === hotel.id
        }).image} /></div></div>
      }


//console.log("selectedHotel", selectedHotel);

      return (<Row>
          <Col md={9}>

            <div className="panel panel-default">
              <div className="panel-heading">Hotels in {this.props.city}</div>
              <div className="panel-body" style={{minHeight: '100px'}}>
                <Loader loaded={!this.state.loading}>
                  <Table striped bordered condensed hover>
                    <thead>
                      <tr>
                        <th>Hotel name</th>
                        <th>Address</th>
                        <th>Locality</th>
                        <th>ZIP code</th>
                        <th>Rating</th>
                        <th>Price</th>
                        <th>Image</th>
                      </tr>
                    </thead>

                    <tbody>
                      {rows}
                    </tbody>

                  </Table>
                </Loader>
              </div>
            </div>
          </Col>
          <Col md={3}>
            {selectedHotel}
          </Col>
        </Row>);



  }
}

export default Hotels;
