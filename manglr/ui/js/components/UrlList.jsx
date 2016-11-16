
class UrlList extends React.Component {
    
    urlItems = this.props.urls.map((urlItem) =>
        <UrlItem urlId={urlItem.urlId} url={urlItem.url} aliases={urlItem.aliases} />
    );

    constructor(props) {
        super(props)
        
    }

    render() {
        return (
            <table>
                <th>
                    <tr>Short</tr>
                    <tr>URL</tr>
                    <tr></tr>
                </th>
                
                {urlItems}

            </table>
        );
    }
}
