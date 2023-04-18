import React from "react";
import "./ArticleContent.css";
import { NotificationManager as nm } from "react-notifications";
import { getRequest } from "../../../utils/request.jsx";
import FormLine from "../../button/FormLine.jsx";
import Loading from "../../box/Loading.jsx";
import Message from "../../box/Message.jsx";
import LogArticleVersion from "../LogArticleVersion.jsx";
import DialogArticleEditor from "./DialogArticleEditor.jsx";
import { getContentFromBlock } from "../../../utils/article.jsx";

export default class ArticleContent extends React.Component {
	constructor(props) {
		super(props);

		this.refresh = this.refresh.bind(this);
		this.getContent = this.getContent.bind(this);
		this.changeState = this.changeState.bind(this);

		this.state = {
			versions: null,
			selectedVersion: null,
			content: null,
			logs: null,
		};
	}

	componentDidMount() {
		this.refresh();
	}

	componentDidUpdate(prevProps, prevState) {
		if (prevState.selectedVersion !== this.state.selectedVersion
			&& this.state.selectedVersion !== null) {
			this.getContent(this.state.selectedVersion);
		}
	}

	refresh() {
		this.setState({
			versions: null,
			logs: null,
		});

		getRequest.call(this, "article/get_article_versions/" + this.props.id, (data) => {
			const mainVersions = data.filter((v) => v.is_main);

			this.setState({
				versions: data,
				selectedVersion: mainVersions.length > 0
					? mainVersions[0].id
					: null,
			});
		}, (response) => {
			nm.warning(response.statusText);
		}, (error) => {
			nm.error(error.message);
		});
	}

	getContent(versionId) {
		getRequest.call(this, "article/get_article_version_content/" + versionId, (data) => {
			this.setState({
				content: data,
			}, () => {
				getRequest.call(this, "log/get_update_article_version_logs/" + versionId, (data2) => {
					this.setState({
						logs: data2.reverse(),
					});
				}, (response) => {
					nm.warning(response.statusText);
				}, (error) => {
					nm.error(error.message);
				});
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
		if (this.state.versions === null) return <Loading height={300}/>;

		return (
			<div className={"ArticleContent row"}>
				<div className="col-md-12">
					<div className={"row"}>
						<div className="col-md-12">
							<h2>Content</h2>
						</div>
					</div>

					{!this.props.node
						&& <div className={"row row-spaced"}>
							<div className="col-md-12">
								<h3>Select version</h3>
							</div>
							<div className="col-md-12">
								<FormLine
									label={"Select version to edit"}
									type={"select"}
									value={this.state.selectedVersion}
									options={[{ value: null, label: "-" }].concat(
										this.state.versions.map((v) => ({ label: v.name, value: v.id })),
									)}
									onChange={(v) => this.changeState("selectedVersion", v)}
								/>
							</div>
						</div>
					}

					<div className={"row row-spaced"}>
						<div className="col-md-12">
							<h3>Content</h3>

							{!this.props.node
								&& <div className={"top-right-buttons"}>
									<DialogArticleEditor
										trigger={<button className={"blue-background"}>
											<i className="far fa-edit"/> Edit the content
										</button>}
										articleVersion={this.state.selectedVersion}
									/>
								</div>
							}
						</div>
					</div>

					{this.state.selectedVersion && this.state.content
						&& this.state.content.length > 0
						&& <div className={"row"}>
							<div className="col-md-12">
								{this.state.content !== null
									&& this.state.content.map((item) => getContentFromBlock(item))
								}
							</div>
						</div>
					}

					{this.state.selectedVersion && this.state.content
						&& this.state.content.length === 0
						&& <div className={"row"}>
							<div className="col-md-12">
								<Message
									height={100}
									text={"No content found"}
								/>
							</div>
						</div>
					}

					{(!this.state.selectedVersion || !this.state.content)
						&& <Loading
							height={150}
						/>
					}

					{!this.props.node
						&& <div className={"row row-spaced"}>
							<div className="col-md-12">
								<h3>History</h3>
							</div>

							{this.state.selectedVersion !== null && this.state.logs !== null
								&& <div className="col-md-12">
									{this.state.logs.length > 0
										? this.state.logs.map((l, i) => (
											<LogArticleVersion
												key={l.id}
												log={l}
												previousLog={this.state.logs[i + 1]}
											/>
										))
										: <Message
											height={100}
											text={"No log in history"}
										/>
									}
								</div>
							}

							{this.state.selectedVersion !== null && this.state.logs === null
								&& <div className="col-md-12">
									<Loading
										height={150}
									/>
								</div>
							}
						</div>
					}
				</div>
			</div>
		);
	}
}
