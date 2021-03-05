import React from "react";
import "./App.css";
import "./css/medium-editor.css";
import { NotificationContainer } from "react-notifications";
import "react-notifications/lib/notifications.css";
import { BrowserRouter } from "react-router-dom";
import InsideApp from "./component/InsideApp";
import Login from "./component/Login";

export default class App extends React.Component {
	constructor(props) {
		super(props);

		this.connect = this.connect.bind(this);

		this.state = {
			logged: false,
		};
	}

	componentDidMount() {
	}

	componentDidUpdate(prevProps, prevState, snapshot) {
	}

	connect() {
		this.setState({
			logged: true,
		});
	}

	render() {
		return (
			<div id="App">
				{this.state.logged
					? <BrowserRouter>
						<InsideApp/>
					</BrowserRouter>
					: <Login
						connect={this.connect}
					/>
				}
				<NotificationContainer/>
			</div>
		);
	}
}
