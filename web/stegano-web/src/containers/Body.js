import React, { Component } from 'react';
import PropTypes from 'prop-types';
import { withStyles } from '@material-ui/core/styles';
import { Grid, Button, Paper, TextField, Checkbox, FormGroup, FormControlLabel } from '@material-ui/core';
import NavigationButtons from '../components/NavigationButtons';
import ReactAudioPlayer from 'react-audio-player';
import { saveAs } from 'file-saver';
import {} from 'save-file';
import download from 'download-file'
import axios from 'axios';


const HOST_ADDRESS = "http://localhost:5000";
const ENCRYPT_ADDRESS = HOST_ADDRESS + "/encrypt";
const DECRYPT_ADDRESS = HOST_ADDRESS + "/decrypt";

const styles = {
	root: {
		flexGrow: 1,
	},
	Typography: {
		textAlign: "center",
	},
	menuButton: {
		marginLeft: -12,
		marginRight: 20,
	},
	bordered: {
		border: "1px solid black"
	},
	Paper: {
		paddingBottom: "20px"
	}
};

class Body extends Component {
	constructor(props) {
		super(props);
		this.state = {
			stegoKey: "",
			randomSequence: false,
			messageEncryption: false,
			containerFileName: "",
			messageFileName: "",
			messageSrc: null,
			containerFileUpload: null,
			messageFileUpload: null,
			audioSrc: null,
			audioSrcOri: null,
			psnr: null,
		}
	}

	async handleEncrypt() {
		if (!this.validateEncrypt()) {
			return;
		}
		console.log(`Encrypting.. Key:${this.state.stegoKey}; ContainerFile: ${this.state.containerFileUpload}; MessageFile: ${this.state.messageFileUpload};Encryption:${this.state.messageEncryption}; RandomSequence:${this.state.randomSequence}  `)
		if (this.state.containerFileUpload && this.state.messageFileUpload) {
			this.setState({ audioSrc: null });
			const { stegoKey, randomSequence, messageEncryption, containerFileUpload, messageFileUpload, containerFileName, messageFileName } = this.state;
			// axios.get(ENCRYPT_ADDRESS);
			var formData = new FormData();
			formData.append('stegoKey', stegoKey);
			formData.append('randomSequence', randomSequence);
			formData.append('messageEncryption', messageEncryption);
			formData.append('containerFile', containerFileUpload, containerFileName);
			formData.append('messageFile', messageFileUpload, messageFileName);
			await axios.post(ENCRYPT_ADDRESS,
				formData,
				{
					headers: {
						'Content-Type': 'multipart/form-data'
					}
				}
			).then(resp => {
				console.log("Status: ", resp.status);
				console.log("Response: ", resp.data);
				var paths = resp.data.split("|");
				this.setState({ audioSrc: paths[1], audioSrcOri: paths[0], psnr: paths[2] });
				// this.render();
			}).catch(error => {
				console.log("Error");
				if (error.response.status == 500){
					alert(error.response.data)
				}
			});
			console.log(`Encrypting.. Key:${this.state.stegoKey}; ContainerFile: ${this.state.containerFileUpload}; MessageFile: ${this.state.messageFileUpload};Encryption:${this.state.messageEncryption}; RandomSequence:${this.state.randomSequence}  `)
			console.log(`Encrypting.. Key:${this.state.stegoKey}; ContainerFile: ${this.state.containerFileUpload}; MessageFile: ${this.state.messageFileUpload};Encryption:${this.state.messageEncryption}; RandomSequence:${this.state.randomSequence}  `)
		}
	}

	renderEncryption() {
		if (this.state.audioSrc) {
			console.log("Src: ", this.state.audioSrc);
			var format = this.state.audioSrc.split(".");
			format = format[format.length - 1];
			return <Grid container>
				<Grid item xs={6}>
					<h4>Original</h4>
					<ReactAudioPlayer
						src={this.state.audioSrcOri}
						controls
					/>
				</Grid>
				<Grid item xs={6}>
					<h4>StegoFile | PSNR : {this.state.psnr}</h4>
					<ReactAudioPlayer
						src={this.state.audioSrc}
						controls
					/>
					<Button color="primary" onClick={()=>{
						var file_name = prompt("Please input file name:", "default");
						if (file_name == null || file_name == "") {
							file_name = "default";
						}
						console.log("URL: ",this.state.audioSrc);
						saveAs(this.state.audioSrc, file_name + "." + format);
						}}>Save StegoFile</Button>
				</Grid>
			</Grid>
		}
	}
	renderDecryption() {
		if (this.state.messageSrc) {
			console.log("MsgSrc: ", this.state.messageSrc);
			var format = this.state.messageSrc.split(".");
			format = format[format.length - 1];
			return <div>
				<Button onClick={() => {
					var file_name = prompt("Please input file name:", "default");
					if (file_name == null || file_name == "") {
						file_name = "default";
					}
					saveAs(this.state.messageSrc, file_name + "." + format);
				}}>Download</Button>
			</div>
		}
	}

	validateDecrypt() {
		if (this.state.stegoKey.length <= 0 || this.state.stegoKey > 25) {
			alert("Stego key must in range [1..25]")
			return false;
		}
		if (!this.state.containerFileUpload) {
			alert("File container must not empty");
			return false
		}
		return true;
	}
	validateEncrypt() {
		if (this.state.stegoKey.length <= 0 || this.state.stegoKey > 25) {
			alert("Stego key must in range [1..25]")
			return false;
		}
		if (!this.state.containerFileUpload) {
			alert("File container must not empty");
			return false
		}
		if (!this.state.messageFileUpload) {
			alert("Message file must not be empty");
			return false;
		}
		return true;
	}

	async handleDecrypt() {
		if (!this.validateDecrypt()) {
			return;
		}
		console.log(`Decrypting Key:${this.state.stegoKey}; ContainerFile: ${this.state.containerFileUpload};   `)
		if (this.state.containerFileUpload) {
			this.setState({ messageSrc: null });
			const { stegoKey, containerFileUpload, containerFileName } = this.state;
			var formData = new FormData();
			formData.append('stegoKey', stegoKey);
			formData.append('containerFile', containerFileUpload, containerFileName);
			await axios.post(DECRYPT_ADDRESS,
				formData,
				{
					headers: {
						'Content-Type': 'multipart/form-data'
					}
				}
			).then(resp => {
				console.log("Status: ", resp.status);
				console.log("Response: ", resp.data)
				this.setState({ messageSrc: resp.data });
			});
		}

	}

	render() {
		const { classes } = this.props;
		return (
			<div className={classes.root}>
				<Paper className={classes.Paper}>
					<Grid container alignContent="space-around" justify="space-around" direction="row" >
						<Grid item xs={12} className={classes.bordered}>
							<NavigationButtons />
						</Grid>
						<Grid item xs={12}>
							<Grid container alignItems="center" direction="column" spacing={16}>
								<Grid item xs={12}>
									<TextField
										id="outlined-name"
										label="Stego Key"
										className={classes.textField}
										value={this.state.stegoKey}
										onChange={(evt) => this.setState({ stegoKey: evt.target.value })}
										margin="normal"
										variant="outlined"
									/>
								</Grid>
								<Grid item xs={12}>
									<p>Container File:</p>
									<input type="file" onChange={(e) => {
										if (e.target.files[0]) {

											this.setState({ containerFileUpload: e.target.files[0], containerFileName: e.target.files[0].name })
										}
									}
									}
									/>
								</Grid>
								<Grid item xs={12}>
									<p>Message File:</p>
									<input type="file" onChange={(e) => {
										if (e.target.files[0]) {
											this.setState({ messageFileUpload: e.target.files[0], messageFileName: e.target.files[0].name })
										}

									}
									} />
								</Grid>
								<Grid item xs={12}>
									Options:
									<FormGroup>
										<FormControlLabel
											control={
												<Checkbox
													checked={this.state.messageEncryption}
													onChange={() => this.setState(prevState => ({ messageEncryption: !prevState.messageEncryption }))}
													color="primary"
												/>
											}
											label="Message Encryption"
										/>
										<FormControlLabel
											control={
												<Checkbox
													checked={this.state.randomSequence}
													onChange={() => this.setState(prevState => ({ randomSequence: !prevState.randomSequence }))}
													color="primary"
												/>
											}
											label="Random Sequence"
										/>
									</FormGroup>
								</Grid>
								<Grid item xs={12}>
									<Grid container spacing={16}>
										<Grid item xs={6}>
											<Button onClick={() => this.handleEncrypt()} variant="outlined" color="primary" className={classes.button}>
												Stego!
      						</Button>
										</Grid>
										<Grid item xs={6}>
											<Button onClick={() => this.handleDecrypt()} variant="outlined" color="secondary" className={classes.button}>
												Extract!
									</Button>
										</Grid>
									</Grid>
								</Grid>
								<Grid item xs={12}>
									{this.renderEncryption()}
								</Grid>
								<Grid item xs={12}>
									{this.renderDecryption()}
								</Grid>
							</Grid>
						</Grid>
					</Grid>
				</Paper>
			</div>
		)
	}
}

Body.propTypes = {
	classes: PropTypes.object.isRequired,
};

export default withStyles(styles)(Body);
