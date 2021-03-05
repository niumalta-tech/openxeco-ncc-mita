import React from "react";
import "./TaskRequest.css";
import { NotificationManager as nm } from "react-notifications";
import Loading from "../box/Loading";
import Message from "../box/Message";
import Table from "../table/Table";
import Request from "../item/Request";
import { getRequest, postRequest } from "../../utils/request";
import FormLine from "../button/FormLine";
import DialogConfirmation from "../dialog/DialogConfirmation";
import CheckBox from "../button/CheckBox";
import { dictToURI } from "../../utils/url";

export default class TaskRequest extends React.Component {
	constructor(props) {
		super(props);

		this.refresh = this.refresh.bind(this);

		const today = new Date();

		this.state = {
			requests: null,
			showNew: true,
			showInProcess: true,
			showProcessed: false,

			today: new Date().toJSON().slice(0, 10),
			yesterday: new Date(today.valueOf() - (1 * 24 * 60 * 60 * 1000)).toJSON().slice(0, 10),
			lastWeek: new Date(today.valueOf() - (7 * 24 * 60 * 60 * 1000)).toJSON().slice(0, 10),
		};
	}

	componentDidMount() {
		this.refresh();
	}

	componentDidUpdate(prevProps, prevState, snapshot) {
		if (prevState.showNew !== this.state.showNew
			|| prevState.showInProcess !== this.state.showInProcess
			|| prevState.showProcessed !== this.state.showProcessed) {
			this.refresh();
		}
	}

	refresh() {
		this.setState({
			requests: null,
		});

		const filters = {
        	status: [],
		};

		if (this.state.showNew) filters.status.push("NEW");
		if (this.state.showInProcess) filters.status.push("IN PROCESS");
		if (this.state.showProcessed) filters.status.push("PROCESSED");

		getRequest.call(this, "request/get_requests?" + dictToURI(filters), (data) => {
			this.setState({
				requests: data.reverse(),
			});
		}, (response) => {
			nm.warning(response.statusText);
		}, (error) => {
			nm.error(error.message);
		});
	}

	changeState(field, value) {
		this.setState({ [field]: value });
	}

	render() {
		return (
			<div id="TaskRequest" className="max-sized-page fade-in">
				<div className={"row"}>
					<div className="col-md-12">
						<h1>Request</h1>
						<div className="top-right-buttons">
							<button
								onClick={() => this.refresh()}>
								<i className="fas fa-redo-alt"/>
							</button>
						</div>
					</div>
				</div>

				<div className={"row"}>
					<div className="col-md-12">
						<div className="TaskRequest-buttons">
							<CheckBox
								label={"NEW"}
								value={this.state.showNew}
								onClick={(v) => this.changeState("showNew", !this.state.showNew)}
							/>
							<CheckBox
                            	label={"IN PROCESS"}
								value={this.state.showInProcess}
								onClick={(v) => this.changeState("showInProcess", !this.state.showInProcess)}
							/>
							<CheckBox
                            	label={"PROCESSED"}
								value={this.state.showProcessed}
								onClick={(v) => this.changeState("showProcessed", !this.state.showProcessed)}
							/>
						</div>
					</div>
				</div>

				{this.state.requests !== null && this.state.requests.length === 0
					? <div className={"row row-spaced"}>
						<Message
							text={"No request found"}
							height={300}
						/>
					</div>
					: ""}

				{this.state.requests !== null && this.state.requests
					.filter((r) => r.submission_date > this.state.today).length > 0
					? <div className={"row row-spaced"}>
						{this.state.requests !== null
							? <div className="col-md-12">
								<h3>Today</h3>
								{this.state.requests
									.filter((r) => r.submission_date > this.state.today)
									.map((r) => (
										<Request
											info={r}
										/>
				           		))}
							</div>
							: ""}
					</div>
					: ""}

				{this.state.requests !== null && this.state.requests
					.filter((r) => r.submission_date < this.state.today)
					.filter((r) => r.submission_date > this.state.yesterday).length > 0
					? <div className={"row row-spaced"}>
						{this.state.requests !== null
							? <div className="col-md-12">
								<h3>Yesterday</h3>
								{this.state.requests
									.filter((r) => r.submission_date < this.state.today)
									.filter((r) => r.submission_date > this.state.yesterday)
									.map((r) => (
										<Request
											info={r}
										/>
				           		))}
							</div>
							: ""}
					</div>
					: ""}

				{this.state.requests !== null && this.state.requests
					.filter((r) => r.submission_date < this.state.yesterday)
					.filter((r) => r.submission_date > this.state.lastWeek).length > 0
					? <div className={"row row-spaced"}>
						{this.state.requests !== null
							? <div className="col-md-12">
								<h3>Last week</h3>
								{this.state.requests
									.filter((r) => r.submission_date < this.state.yesterday)
									.filter((r) => r.submission_date > this.state.lastWeek)
									.map((r) => (
										<Request
											info={r}
										/>
				           		))}
							</div>
							: ""}
					</div>
					: ""}

				{this.state.requests !== null && this.state.requests
					.filter((r) => r.submission_date < this.state.lastWeek).length > 0
					? <div className={"row row-spaced"}>
						{this.state.requests !== null
							? <div className="col-md-12">
								<h3>Others</h3>
								{this.state.requests
									.filter((r) => r.submission_date < this.state.lastWeek)
									.map((r) => (
										<Request
											info={r}
										/>
				           		))}
							</div>
							: ""}
					</div>
					: ""}
			</div>
		);
	}
}
