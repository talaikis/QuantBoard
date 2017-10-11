// @flow
import React, { Component } from 'react';
import styles from './Home.css';
import Chart from '../utils/Chart';
import { getData } from "../utils/Data"
import { TypeChooser } from "react-stockcharts/lib/helper";

export default class Home extends Component {
  componentDidMount() {
		getData().then(data => {
			this.setState({ data })
		})
	}
  render() {
    if (this.state == null) {
			return <div>Loading...</div>
		}
		return (
			<TypeChooser>
				{type => <Chart type={type} data={this.state.data} />}
			</TypeChooser>
		)
  }
}
