import React, {useState, useEffect} from "react";
import axios from 'axios';
import {useHistory} from 'react-router-dom';
import { AuthContext } from "../App";

const NewRequest = () => {
    const { state } = React.useContext(AuthContext);
    const history = useHistory();
    const [datasets, setDatasets] = useState([]);
    const [dataSource, setDataSource] = useState("")
    const [dataView, setDataView] = useState("")
    const [selectedDataset, selectDataset] = useState(null)
    const months = [1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12]
    const [selectedNumberOfMonths, setSelectedNumberOfMonths] = useState(0)
    const [extractionCost, setExtractionCost] = useState(0)
    const handleRadioChange1 = event => {
        setDataSource(event.target.id)
    };
    const handleRadioChange2 = event => {
        setDataView(event.target.id)        
    };
    const handleRadioChange3 = event => {
        let keyId = event.target.id
        selectDataset(datasets.find(dataset => {
            return dataset.id === keyId
        }))
    };
    const handleRadioChange4 = event => {
        setSelectedNumberOfMonths(event.target.id)
    };
    
    useEffect(() => {
        const fetchExtractionCost = async () => {
          const response = await axios.post('http://127.0.0.1:5000/predictCost', {
            userscope: 'Personal',
            entityName: selectedDataset ? selectedDataset.entityName:'',
            daysSelected: selectedNumberOfMonths === 0 ? 180: selectedNumberOfMonths*30
          })
          setExtractionCost(response.data)
        }
        fetchExtractionCost()
      }, [selectedNumberOfMonths, selectedDataset])

    const handleSubmission = event => {
        event.preventDefault()

        axios.post("http://127.0.0.1:5000/newRequest", {
            requestName: dataView+dataSource,
            userId: state.userid,
            datasetName: selectedDataset.entityName,
            datasetId: selectedDataset.id,
            datasetScope: dataSource,
            daysSelected: parseInt(selectedNumberOfMonths)*30,
        })
        .then(response => {
            history.push("/")
        })
        .catch(error => {
            // console.log(error.response);
        });
    }
    useEffect(() => {
        const fetchRequests = async () => {
          const response = await axios.get("http://127.0.0.1:5000/getDatasets");
          let tempVar = response.data
          setDatasets(tempVar);
        }
        fetchRequests();
      }, []);
    return (
        <>
            <form>
                <h3>Data source and dataset</h3>
                <div className="form-group">
                    <label>Select a data source</label>
                    <div className="form-check">
                        <input type="radio" className="form-check-input" id="personal" name="datasource" onChange={handleRadioChange1} checked={dataSource==="personal"}/>
                        <label className="form-check-label" htmlFor="personal">My Office365 Data</label>
                    </div>
                    <div className="form-check">
                        <input type="radio" className="form-check-input" id="publicGroup" name="datasource" onChange={handleRadioChange1} checked={dataSource==="publicGroup"}/>
                        <label className="form-check-label" htmlFor="publicGroup">Office365 Public Groups</label>
                    </div>            
                </div>
                <div className="form-group">
                    <label>Select a view</label>
                    <div className="form-check">
                        <input type="radio" className="form-check-input" id="SubstrateML" name="view" onChange={handleRadioChange2} checked={dataView==="SubstrateML"}/>
                        <label className="form-check-label" htmlFor="substrateml">SubstrateML (curated)</label>
                    </div>
                    <div className="form-check">
                        <input type="radio" className="form-check-input" id="MSGraph" name="view" onChange={handleRadioChange2} checked={dataView==="MSGraph"}/>
                        <label className="form-check-label" htmlFor="msgraph">MSGraph (raw)</label>
                    </div>            
                </div>
            </form>
            <table className="table table-striped">
                <thead>
                <tr>
                    <th>-</th>
                    <th>View</th>
                    <th>Description</th>
                    <th>Requested</th>
                    <th>Extracted</th>
                    <th>User Completeness</th>
                </tr>
                </thead>
                <tbody>
            {(datasets && dataSource && dataView) ?
                datasets.map(dataset => (
                        (dataset.datasetName === dataView && ((dataset.datasetUserScope.personal === "1" && dataSource==="personal") || (dataset.datasetUserScope.publicGroup === "1" && dataSource==="publicGroup"))) ? 
                    <tr key={dataset.id}>
                        <td>
                            <div className="form-check">
                                <input id={dataset.id} type="radio" className="form-check-input" name="selectDataset" onChange={handleRadioChange3}/>
                            </div>
                        </td>
                        <td>{dataset.entityName}</td>
                        <td>{dataset.description}</td>
                        <td>{dataset.numberOfRequests}</td>
                        <td>{dataset.successfulExtractions}</td>
                        <td>{dataset.userCompleteness}</td>
                    </tr>:null
            )):null}
                </tbody>
            </table>
            {selectedDataset === null? null:(
                <form>
                    <h3>Select Date Range for {selectedDataset.entityName}</h3>
                    <div className="form-group">
                        <label>Select a range</label>
                        {
                            months.map(num => (
                                (num <= (parseInt(selectedDataset.datasetAvailability)/30)) ? 
                                <div className="form-check" key={num}>
                                    <input id={num} type="radio" className="form-check-input" name="range" onChange={handleRadioChange4}/>
                                    <label className="form-check-label" htmlFor="range">{num} months</label>
                                </div> : null
                            ))
                            
                        }
                    </div>
                    {
                        extractionCost &&  <h3>Estimated Time (hours) = {extractionCost}</h3>
                    }
                </form>
            )
            }
            {
                selectedNumberOfMonths ? (
                    <button type="submit" className="btn btn-primary btn-block" onClick={handleSubmission}>Submit New Request</button>
                ):null
            }
        </>
    );
}

export default NewRequest